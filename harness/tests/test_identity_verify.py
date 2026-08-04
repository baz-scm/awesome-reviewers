"""Pillars 5 and 6 together, plus the whole pipeline.

The end-to-end tests run a real plan in a throwaway repository and then attack the
record: rewrite a ledger entry, truncate the chain, corrupt a blob, edit the policy
pack. Each attack must be caught by a named check, and none of them may leave
`verify` reporting success.

The identity tests pin down the one distinction the pillar rests on: a claim about
who ran something is never reported as proof.
"""

from __future__ import annotations

import json
import os
import unittest
from pathlib import Path
from unittest import mock

from awesome_harness.errors import ApprovalRequired, ConfigError, GateFailed, IntegrityError
from awesome_harness.identity import (
    AGENT_MARKERS,
    PREDICATE_TYPE,
    SIGNATURE_UNSIGNED,
    SIGNATURE_VALID,
    STATEMENT_TYPE,
    Actor,
    Envelope,
    Signer,
    build_statement,
    commit_trailers,
    resolve_actor,
    statement_bytes,
)
from awesome_harness.ledger import Ledger
from awesome_harness.plan import Plan, Runner, approval_token
from awesome_harness.policy import Corpus, build_pack, save_pack
from awesome_harness.verify import verify_attestation

from .support import TempRepo

GATE_ONLY_PLAN = {
    "schema": 1,
    "name": "review",
    "phases": [{"name": "review", "gate": True, "steps": []}],
}

BUILD_PLAN = {
    "schema": 1,
    "name": "build",
    "phases": [
        {
            "name": "build",
            "gate": False,
            "steps": [
                {
                    "id": "emit",
                    "run": ["python3", "-c", "open('out.txt','w').write('built\\n')"],
                    "inputs": ["src.py"],
                    "tools": ["python3 --version"],
                    "outputs": [{"path": "out.txt"}],
                }
            ],
        }
    ],
}

APPROVAL_PLAN = {
    "schema": 1,
    "name": "gated",
    "phases": [{"name": "release", "approval": True, "gate": False, "steps": []}],
}


class TestActorResolution(TempRepo):
    def test_git_identity_is_recorded_with_its_evidence(self) -> None:
        actor = resolve_actor(self.root)
        self.assertEqual(actor.email, "test@example.invalid")
        self.assertTrue(any("git config" in note for note in actor.evidence))

    def test_an_agent_marker_is_a_claim_with_the_variable_named(self) -> None:
        # Every other agent marker is cleared: this test runs inside a coding agent
        # often enough that an ambient CLAUDECODE would otherwise win precedence.
        cleared = {name: "" for name, _ in AGENT_MARKERS}
        with mock.patch.dict(os.environ, {**cleared, "AWESOME_HARNESS_AGENT": "1"}, clear=False):
            actor = resolve_actor(self.root, declared_model="some-model-5")
        self.assertEqual(actor.kind, "agent")
        self.assertEqual(actor.agent["observed_via"], "AWESOME_HARNESS_AGENT")  # type: ignore[index]
        self.assertTrue(any("environment marker" in note for note in actor.evidence))

    def test_trailers_carry_run_and_actor(self) -> None:
        actor = Actor(kind="agent", id="agent:test", agent={"tool": "t", "model": "m-1"})
        trailers = commit_trailers(actor, run_id="r-1", attestation_digest="sha256:" + "a" * 64)
        joined = "\n".join(trailers)
        self.assertIn("Harness-Run-Id: r-1", joined)
        self.assertIn("Harness-Agent-Model: m-1", joined)
        self.assertIn("Harness-Attestation: sha256:", joined)


class TestStatement(unittest.TestCase):
    def _statement(self, head: str = "sha256:" + "a" * 64) -> dict:
        return build_statement(
            run_id="r-1",
            subjects=[{"name": "out.txt", "digest": {"sha256": "b" * 64}}],
            plan={"plan": "p"},
            actor=Actor(kind="human", id="human:a@b", email="a@b"),
            scm={"head": "c" * 40, "branch": "main", "snapshot_commit": "d" * 40, "snapshot_tree": "e" * 40},
            policy={"pack": "default", "packDigest": "sha256:" + "f" * 64, "verdict": "pass"},
            steps=[],
            isolation={"backend": "local"},
            ledger_head=head,
            started="2026-01-01T00:00:00Z",
        )

    def test_shape_is_in_toto_statement_v1(self) -> None:
        statement = self._statement()
        self.assertEqual(statement["_type"], STATEMENT_TYPE)
        self.assertEqual(statement["predicateType"], PREDICATE_TYPE)

    def test_git_object_ids_are_labelled_sha1_not_sha256(self) -> None:
        # A 40-hex git oid labelled sha256 makes a verifier compare a commit id against
        # a content hash and conclude, correctly but uselessly, that nothing matches.
        deps = self._statement()["predicate"]["buildDefinition"]["resolvedDependencies"]
        self.assertTrue(deps)
        for dependency in deps:
            self.assertIn("sha1", dependency["digest"])
            self.assertNotIn("sha256", dependency["digest"])

    def test_policy_is_a_first_class_predicate_field(self) -> None:
        predicate = self._statement()["predicate"]
        self.assertEqual(predicate["policy"]["pack"], "default")
        self.assertEqual(predicate["policy"]["verdict"], "pass")

    def test_statement_is_a_pure_function_of_its_arguments(self) -> None:
        self.assertEqual(statement_bytes(self._statement()), statement_bytes(self._statement()))


class TestEnvelope(TempRepo):
    def test_an_unsigned_envelope_says_so_in_the_file(self) -> None:
        envelope = Envelope(payload=b'{"a":1}', unsigned_reason="no key configured")
        payload = envelope.to_json()
        self.assertEqual(payload["signatureStatus"], SIGNATURE_UNSIGNED)
        self.assertEqual(payload["unsignedReason"], "no key configured")
        self.assertEqual(payload["signatures"], [])

    def test_round_trip_preserves_the_payload_bytes(self) -> None:
        original = Envelope(payload=b'{"z":[1,2,3]}')
        restored = Envelope.from_json(original.to_json())
        self.assertEqual(restored.payload, original.payload)
        self.assertEqual(restored.statement(), {"z": [1, 2, 3]})

    def test_a_payload_digest_that_does_not_match_is_refused(self) -> None:
        payload = Envelope(payload=b'{"a":1}').to_json()
        payload["payloadDigest"] = "sha256:" + "0" * 63 + "1"
        with self.assertRaises(IntegrityError):
            Envelope.from_json(payload)

    def test_a_bad_payload_type_is_refused(self) -> None:
        payload = Envelope(payload=b"{}").to_json()
        payload["payloadType"] = "text/plain"
        with self.assertRaises(ConfigError):
            Envelope.from_json(payload)

    def test_signing_without_a_key_degrades_visibly_and_never_fabricates(self) -> None:
        signer = Signer(key="", namespace="test")
        available, reason = signer.available()
        self.assertFalse(available)
        envelope = signer.sign(b"payload", scratch=self.ws.tmp_dir)
        self.assertEqual(envelope.signatures, [])
        self.assertIn(reason, envelope.unsigned_reason)


class RunFixture(TempRepo):
    """A completed run, ready to be attacked."""

    plan_body: dict = GATE_ONLY_PLAN

    def setUp(self) -> None:
        super().setUp()
        pack = build_pack(Corpus(self.corpus), name="default", limit=20, topics=["Security"])
        save_pack(self.ws.policy_dir, pack)
        self.pack = pack
        self.write("src.py", "VALUE = 1\n")
        self.plan_path = self.write("plan.json", json.dumps(self.plan_body))
        self.plan = Plan.load(self.plan_path)

    def run_plan(self, **kwargs):  # type: ignore[no-untyped-def]
        return Runner(self.ws, **kwargs).run(self.plan)

    @property
    def attestation(self) -> Path:
        return sorted(self.ws.attestations_dir.glob("*.json"))[-1]


class TestEndToEnd(RunFixture):
    def test_a_clean_run_produces_a_verifiable_record(self) -> None:
        result = self.run_plan()
        self.assertEqual(result.status, "passed")
        self.assertIsNotNone(result.snapshot)
        self.assertEqual(result.gate["verdict"], "pass")  # type: ignore[index]

        report = verify_attestation(self.ws, self.attestation)
        self.assertEqual(report.failures, [], report.render())
        # Unsigned here because ssh-keygen may not exist; that is reported as its own
        # state and must never read as verified.
        self.assertIn(report.signature, (SIGNATURE_UNSIGNED, SIGNATURE_VALID))
        names = {check["check"] for check in report.checks}
        self.assertLessEqual(
            {"envelope", "statement", "ledger-chain", "ledger-anchor", "subjects", "policy-pack", "policy-verdict", "signature"},
            names,
        )

    def test_the_ledger_records_the_whole_run_in_order(self) -> None:
        self.run_plan()
        types = [record.type for record in Ledger(self.ws.ledger_dir).read_all()]
        self.assertEqual(types[0], "RUN_STARTED")
        self.assertEqual(types[1], "SNAPSHOT_CREATED")
        self.assertIn("GATE_EVALUATED", types)
        self.assertEqual(types[-2:], ["ATTESTATION_CREATED", "RUN_FINISHED"])

    def test_the_run_folder_holds_the_gate_report_and_the_context_bundle(self) -> None:
        result = self.run_plan()
        assert result.run_dir is not None
        self.assertTrue((result.run_dir / "gate.json").is_file())
        bundle = (result.run_dir / "review-context.md").read_text(encoding="utf-8")
        self.assertIn("Review context", bundle)

    def test_the_worktree_is_torn_down(self) -> None:
        result = self.run_plan()
        assert result.run_dir is not None
        self.assertFalse((result.run_dir / "work").exists())

    def test_a_failing_gate_still_writes_an_attestation(self) -> None:
        # The run whose provenance someone most wants to read is the one that failed.
        self.write("leak.py", 'KEY = "AKIAIOSFODNN7EXAMPLE"\n')
        with self.assertRaises(GateFailed):
            self.run_plan()
        statement = Envelope.from_json(json.loads(self.attestation.read_text(encoding="utf-8"))).statement()
        self.assertEqual(statement["predicate"]["policy"]["verdict"], "fail")

        report = verify_attestation(self.ws, self.attestation)
        verdict_check = next(c for c in report.checks if c["check"] == "policy-verdict")
        self.assertFalse(verdict_check["ok"])

    def test_advisory_only_records_the_downgrade(self) -> None:
        self.write("leak.py", 'KEY = "AKIAIOSFODNN7EXAMPLE"\n')
        result = self.run_plan(advisory_only=True)
        self.assertEqual(result.status, "passed")
        statement = Envelope.from_json(json.loads(self.attestation.read_text(encoding="utf-8"))).statement()
        self.assertTrue(
            statement["predicate"]["buildDefinition"]["externalParameters"]["advisoryOnly"],
            "a softened gate must be visible in the record",
        )


class TestTamperMatrix(RunFixture):
    def setUp(self) -> None:
        super().setUp()
        self.run_plan()
        self.ledger = Ledger(self.ws.ledger_dir)

    def _report(self):  # type: ignore[no-untyped-def]
        return verify_attestation(self.ws, self.attestation)

    def _failed(self, name: str) -> dict:
        report = self._report()
        failures = {check["check"]: check for check in report.failures}
        self.assertIn(name, failures, f"expected {name} to fail; got {report.render()}")
        self.assertFalse(report.ok)
        return failures[name]

    def test_rewriting_a_ledger_record_breaks_the_chain(self) -> None:
        lines = self.ledger.path.read_text(encoding="utf-8").strip().split("\n")
        record = json.loads(lines[1])
        record["body"]["tree"] = "0" * 40
        lines[1] = json.dumps(record, separators=(",", ":"), sort_keys=True)
        self.ledger.path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        self.assertIn("record 2", self._failed("ledger-chain")["detail"])

    def test_truncate_and_rechain_is_caught_by_the_record_count(self) -> None:
        # Re-chaining a truncated ledger can reproduce a matching head. It cannot
        # reproduce the head at the sequence number the statement recorded.
        records = self.ledger.read_all()
        keep = records[:-3]
        self.ledger.path.write_text(
            "\n".join(json.dumps(r.to_json(), separators=(",", ":"), sort_keys=True) for r in keep) + "\n",
            encoding="utf-8",
        )
        detail = self._failed("ledger-anchor")["detail"]
        self.assertTrue("not in the ledger" in detail or "statement recorded" in detail, detail)

    def test_corrupting_an_artifact_blob_is_caught(self) -> None:
        # gate-only runs publish nothing, so publish something first.
        from awesome_harness.artifacts import Store

        store = Store(self.ws.artifacts_dir)
        artifact = store.put_file(self.write("thing.bin", "payload\n"), name="thing.bin")
        statement_path = self.attestation
        payload = json.loads(statement_path.read_text(encoding="utf-8"))
        envelope = Envelope.from_json(payload)
        statement = envelope.statement()
        statement["subject"].append({"name": "thing.bin", "digest": {"sha256": artifact.digest.split(":")[1]}})
        statement_path.write_text(
            json.dumps(Envelope(payload=statement_bytes(statement)).to_json()), encoding="utf-8"
        )
        self.assertEqual(self._report().failures, [], "baseline must verify before tampering")

        blob = store.blob_path(artifact.digest)
        blob.chmod(0o644)
        blob.write_bytes(b"tampered\n")
        self.assertIn("thing.bin", self._failed("subjects")["detail"])

    def test_a_missing_subject_blob_is_caught(self) -> None:
        from awesome_harness.artifacts import Store

        store = Store(self.ws.artifacts_dir)
        payload = json.loads(self.attestation.read_text(encoding="utf-8"))
        statement = Envelope.from_json(payload).statement()
        statement["subject"].append({"name": "never-stored.bin", "digest": {"sha256": "a" * 64}})
        self.attestation.write_text(
            json.dumps(Envelope(payload=statement_bytes(statement)).to_json()), encoding="utf-8"
        )
        self.assertIn("never-stored.bin", self._failed("subjects")["detail"])
        del store

    def test_editing_the_policy_pack_is_caught(self) -> None:
        path = self.ws.policy_dir / "default.pack.json"
        payload = json.loads(path.read_text(encoding="utf-8"))
        payload["rules"] = [r for r in payload["rules"] if r["id"] != "AH001"]
        path.write_text(json.dumps(payload), encoding="utf-8")
        # load_pack refuses an edited file outright, which surfaces as a failed check.
        self.assertIn("modified", self._failed("policy-pack")["detail"])

    def test_swapping_in_a_differently_built_pack_is_caught(self) -> None:
        # A pack that is internally consistent but is not the one that gated the run.
        other = build_pack(Corpus(self.corpus), name="default", limit=5, topics=["CI/CD"])
        save_pack(self.ws.policy_dir, other)
        self.assertIn("statement says", self._failed("policy-pack")["detail"])

    def test_editing_the_statement_payload_is_caught(self) -> None:
        payload = json.loads(self.attestation.read_text(encoding="utf-8"))
        statement = Envelope.from_json(payload).statement()
        statement["predicate"]["policy"]["verdict"] = "pass"
        statement["predicate"]["actor"]["id"] = "human:someone-else"
        # Keep the original (now wrong) payloadDigest: the edit must not slip through.
        payload["payload"] = __import__("base64").b64encode(statement_bytes(statement)).decode("ascii")
        self.attestation.write_text(json.dumps(payload), encoding="utf-8")
        report = self._report()
        self.assertFalse(report.ok)
        self.assertIn("envelope", {check["check"] for check in report.failures})

    def test_corpus_drift_is_reported(self) -> None:
        slug = self.pack.rules[0].slug
        path = self.corpus / f"{slug}.md"
        path.write_text(path.read_text(encoding="utf-8") + "\nRevised guidance.\n", encoding="utf-8")
        self.assertIn("changed or removed", self._failed("corpus-drift")["detail"])


class TestCachingAcrossRuns(RunFixture):
    plan_body = BUILD_PLAN

    def test_the_second_run_replays_from_cache(self) -> None:
        first = self.run_plan()
        self.assertEqual(first.status, "passed")
        self.assertFalse(first.steps[0].cached)
        self.assertEqual(len(first.steps[0].outputs), 1)

        second = self.run_plan()
        self.assertTrue(second.steps[0].cached, "identical inputs must replay")
        self.assertEqual(
            first.steps[0].cache_key, second.steps[0].cache_key, "the key must be stable across runs"
        )
        self.assertEqual(
            [a.digest for a in first.steps[0].outputs], [a.digest for a in second.steps[0].outputs]
        )

    def test_changing_a_declared_input_forces_re_execution(self) -> None:
        first = self.run_plan()
        self.write("src.py", "VALUE = 2\n")
        second = self.run_plan()
        self.assertFalse(second.steps[0].cached)
        self.assertNotEqual(first.steps[0].cache_key, second.steps[0].cache_key)

    def test_no_cache_forces_re_execution_and_says_why(self) -> None:
        self.run_plan()
        again = self.run_plan(no_cache=True)
        self.assertFalse(again.steps[0].cached)
        self.assertIn("disabled", again.steps[0].note)

    def test_cache_hits_are_recorded_in_the_ledger(self) -> None:
        self.run_plan()
        self.run_plan()
        types = [r.type for r in Ledger(self.ws.ledger_dir).read_all()]
        self.assertIn("CACHE_MISS", types)
        self.assertIn("CACHE_HIT", types)


class TestApprovalGate(RunFixture):
    plan_body = APPROVAL_PLAN

    def test_an_unapproved_phase_stops_the_run_with_its_own_exit_code(self) -> None:
        with self.assertRaises(ApprovalRequired) as caught:
            self.run_plan()
        self.assertEqual(caught.exception.exit_code, 8)
        self.assertIn("approve release", str(caught.exception.hint))

    def test_approving_on_the_run_lets_it_proceed(self) -> None:
        result = self.run_plan(approve=["release"])
        self.assertEqual(result.status, "passed")
        types = [r.type for r in Ledger(self.ws.ledger_dir).read_all()]
        self.assertIn("APPROVAL_RECORDED", types)

    def test_an_approval_does_not_carry_over_to_changed_code(self) -> None:
        self.run_plan(approve=["release"])
        # Approval was bound to a tree digest; changing the tree must invalidate it.
        self.write("new_thing.py", "X = 1\n")
        with self.assertRaises(ApprovalRequired):
            self.run_plan()

    def test_a_recorded_approval_is_honoured_on_a_later_run(self) -> None:
        from awesome_harness.scm import Git

        pack_digest = self.pack.digest
        tree = Git(self.root).snapshot("probe", message="probe", tmp_dir=self.ws.tmp_dir).tree
        token = approval_token(
            plan_digest=self.plan.digest, phase="release", tree=tree, pack_digest=pack_digest
        )
        Runner(self.ws).record_approval(token, phase="release", run_id="manual")
        self.assertEqual(self.run_plan().status, "passed")

    def test_an_approval_for_a_different_phase_does_not_count(self) -> None:
        token = approval_token(
            plan_digest=self.plan.digest, phase="something-else", tree="a" * 40, pack_digest=self.pack.digest
        )
        Runner(self.ws).record_approval(token, phase="something-else", run_id="manual")
        with self.assertRaises(ApprovalRequired):
            self.run_plan()


class TestPlanValidation(TempRepo):
    def test_duplicate_phase_names_are_refused(self) -> None:
        from awesome_harness.errors import UsageError

        path = self.write(
            "dup.json",
            json.dumps({"schema": 1, "name": "d", "phases": [{"name": "a"}, {"name": "a"}]}),
        )
        with self.assertRaises(UsageError) as caught:
            Plan.load(path)
        self.assertIn("duplicate phase", str(caught.exception))

    def test_a_plan_with_no_phases_is_refused(self) -> None:
        from awesome_harness.errors import UsageError

        path = self.write("empty.json", json.dumps({"schema": 1, "name": "e", "phases": []}))
        with self.assertRaises(UsageError):
            Plan.load(path)

    def test_a_newer_schema_is_refused_rather_than_guessed_at(self) -> None:
        from awesome_harness.errors import UsageError

        path = self.write(
            "future.json", json.dumps({"schema": 99, "name": "f", "phases": [{"name": "a"}]})
        )
        with self.assertRaises(UsageError):
            Plan.load(path)

    def test_plan_digest_covers_the_steps(self) -> None:
        first = Plan.load(self.write("a.json", json.dumps(BUILD_PLAN)))
        altered = json.loads(json.dumps(BUILD_PLAN))
        altered["phases"][0]["steps"][0]["run"] = ["python3", "-c", "pass"]
        second = Plan.load(self.write("b.json", json.dumps(altered)))
        self.assertNotEqual(first.digest, second.digest)

    def test_approval_token_binds_to_plan_phase_tree_and_pack(self) -> None:
        base = {
            "plan_digest": "sha256:" + "a" * 64,
            "phase": "release",
            "tree": "b" * 40,
            "pack_digest": "sha256:" + "c" * 64,
        }
        token = approval_token(**base)  # type: ignore[arg-type]
        for field, value in (
            ("plan_digest", "sha256:" + "9" * 64),
            ("phase", "other"),
            ("tree", "d" * 40),
            ("pack_digest", "sha256:" + "8" * 64),
        ):
            self.assertNotEqual(
                token, approval_token(**{**base, field: value}), f"{field} must bind"  # type: ignore[arg-type]
            )


if __name__ == "__main__":
    unittest.main()
