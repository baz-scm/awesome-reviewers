"""The runner — where the six pillars become one execution.

A plan is phases, a phase is steps plus an optional gate and an optional human
approval. Phases run in declaration order; steps within a phase run in sequence.
That is deliberately the same shape as AI-DLC's inception → construction →
operations, because the shape is good: named phases with review points between them.

What is different is where the enforcement lives. In a steering-rules methodology
the phase gate is prose the model is asked to honour. Here the gate is code, its
verdict is a ledger record, the approval binds to the digest of the exact tree and
finding set that was approved, and the whole run ends in a signed statement.

Order of operations for one run:

     1  resolve actor, load and digest the policy pack, report corpus drift
     2  RUN_STARTED — git facts, plan digest, pack digest, actor, chosen backend
     3  snapshot the worktree into immutable git objects, anchored to a ref
     4  detached worktree of that snapshot: the isolated compute for every step
     5  per phase: approval -> steps (cache lookup, execute, publish) -> gate
     6  attest: subjects are the artifacts, predicate names the policy that gated them
     7  RUN_FINISHED, then tear down the worktree

Derived from the corpus:
  aidlc-workflows-cicd-workflow-predictability — a run does the same thing in the
      same order every time; conditional stages are declared, not inferred.
  aidlc-workflows-single-transaction-locking — every ledger append is its own
      transaction, so a crash mid-run leaves a valid prefix rather than a fork.
  aidlc-workflows-fail-loudly-degrade-safely — a phase that cannot run stops the
      run with its own exit code instead of being skipped.
  aidlc-workflows-no-silent-null-artifacts — a step that produced nothing it
      declared fails, even if it exited zero.
"""

from __future__ import annotations

import shutil
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable

from . import SCHEMA_VERSION, __version__
from .artifacts import Artifact, Manifest, Store
from .cache import Cache, Entry, limits_from_config
from .digest import digest_file, digest_json, digest_tree
from .errors import ApprovalRequired, ExecutionError, GateFailed, UsageError
from .execution import (
    Step,
    build_env,
    collect_outputs,
    env_fingerprint,
    ledger_body,
    select_sandbox,
    tool_fingerprints,
)
from .identity import (
    Actor,
    Envelope,
    Signer,
    build_statement,
    resolve_actor,
    statement_bytes,
)
from .ledger import (
    APPROVAL_RECORDED,
    ARTIFACT_PUBLISHED,
    ATTESTATION_CREATED,
    CACHE_HIT,
    CACHE_MISS,
    GATE_EVALUATED,
    RUN_FINISHED,
    RUN_STARTED,
    SNAPSHOT_CREATED,
    STAGE_FINISHED,
    STAGE_STARTED,
    STEP_FINISHED,
    STEP_STARTED,
    Ledger,
)
from .paths import ensure_dir
from .policy import (
    Corpus,
    Pack,
    Waivers,
    advisory_bundle,
    build_context,
    evaluate as evaluate_gate,
    load_pack,
    summary as gate_summary,
)
from .scm import Git, Snapshot
from .workspace import Workspace, atomic_write_bytes, atomic_write_json, new_run_id, read_json, utc_now


# --------------------------------------------------------------------------- #
# Plan model
# --------------------------------------------------------------------------- #

@dataclass(frozen=True)
class Phase:
    name: str
    description: str = ""
    steps: tuple[Step, ...] = ()
    # Evaluate the policy gate at the end of this phase.
    gate: bool = False
    # Require a recorded human approval before this phase runs.
    approval: bool = False

    @classmethod
    def parse(cls, raw: dict[str, Any]) -> "Phase":
        if not isinstance(raw, dict) or "name" not in raw:
            raise UsageError(f"phase must be an object with a 'name': {raw!r}")
        return cls(
            name=str(raw["name"]),
            description=str(raw.get("description", "")),
            steps=tuple(Step.parse(s) for s in raw.get("steps", [])),
            gate=bool(raw.get("gate", False)),
            approval=bool(raw.get("approval", False)),
        )

    def identity(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "gate": self.gate,
            "approval": self.approval,
            "steps": [s.identity() for s in self.steps],
        }


@dataclass(frozen=True)
class Plan:
    name: str
    description: str = ""
    phases: tuple[Phase, ...] = ()
    schema: int = SCHEMA_VERSION
    source: str = ""

    @classmethod
    def load(cls, path: Path) -> "Plan":
        raw = read_json(path, what="plan")
        if not isinstance(raw, dict):
            raise UsageError(f"plan must be a JSON object: {path}")
        schema = raw.get("schema", SCHEMA_VERSION)
        if not isinstance(schema, int) or schema > SCHEMA_VERSION:
            raise UsageError(f"plan schema {schema!r} is newer than this harness understands")
        phases = tuple(Phase.parse(p) for p in raw.get("phases", []))
        if not phases:
            raise UsageError(f"plan {path} declares no phases")
        names = [p.name for p in phases]
        duplicates = sorted({n for n in names if names.count(n) > 1})
        if duplicates:
            # Phase names key approvals and the ledger's stage-scoped queries. Two
            # phases sharing a name would make both ambiguous.
            raise UsageError(f"plan {path} has duplicate phase name(s): {', '.join(duplicates)}")
        return cls(
            name=str(raw.get("name", path.stem)),
            description=str(raw.get("description", "")),
            phases=phases,
            schema=schema,
            source=str(path),
        )

    @property
    def digest(self) -> str:
        return digest_json(
            {"schema": self.schema, "name": self.name, "phases": [p.identity() for p in self.phases]}
        )

    def phase(self, name: str) -> Phase:
        for phase in self.phases:
            if phase.name == name:
                return phase
        raise UsageError(
            f"plan {self.name!r} has no phase {name!r}",
            hint=f"phases: {', '.join(p.name for p in self.phases)}",
        )


def approval_token(*, plan_digest: str, phase: str, tree: str, pack_digest: str) -> str:
    """What an approval is bound to.

    The plan, the phase, the exact source tree, and the policy that will gate it.
    Change any one of them and the approval no longer applies — which is the whole
    difference between a sign-off and a checkbox.
    """
    return digest_json({"plan": plan_digest, "phase": phase, "tree": tree, "pack": pack_digest})


# --------------------------------------------------------------------------- #
# Results
# --------------------------------------------------------------------------- #

@dataclass
class StepOutcome:
    step: str
    exit_code: int
    duration_ms: int
    cached: bool
    backend: str
    cache_key: str
    outputs: list[Artifact] = field(default_factory=list)
    redactions: list[str] = field(default_factory=list)
    note: str = ""

    def to_json(self) -> dict[str, Any]:
        payload = {
            "id": self.step,
            "exit_code": self.exit_code,
            "duration_ms": self.duration_ms,
            "outcome": "replayed" if self.cached else "executed",
            "backend": self.backend,
            "cache_key": self.cache_key,
            "outputs": [{"name": a.name, "digest": a.digest, "size": a.size} for a in self.outputs],
        }
        if self.redactions:
            payload["redactions"] = self.redactions
        if self.note:
            payload["note"] = self.note
        return payload


@dataclass
class RunResult:
    run_id: str
    status: str
    plan: str
    snapshot: Snapshot | None
    steps: list[StepOutcome] = field(default_factory=list)
    gate: dict[str, Any] | None = None
    attestation: Path | None = None
    signature: str = "unsigned"
    run_dir: Path | None = None
    backend_note: str = ""
    drift: list[dict[str, str]] = field(default_factory=list)

    def to_json(self) -> dict[str, Any]:
        return {
            "run_id": self.run_id,
            "status": self.status,
            "plan": self.plan,
            "snapshot": {
                "tree": self.snapshot.tree,
                "commit": self.snapshot.commit,
                "ref": self.snapshot.ref,
                "changed": list(self.snapshot.changed),
            }
            if self.snapshot
            else None,
            "steps": [s.to_json() for s in self.steps],
            "gate": self.gate,
            "attestation": str(self.attestation) if self.attestation else None,
            "signature": self.signature,
            "backend": self.backend_note,
            "corpus_drift": self.drift,
        }


# --------------------------------------------------------------------------- #
# Runner
# --------------------------------------------------------------------------- #

class Runner:
    def __init__(
        self,
        workspace: Workspace,
        *,
        base: str | None = None,
        advisory_only: bool = False,
        approve: Iterable[str] = (),
        no_cache: bool = False,
        keep_worktree: bool = False,
        declared_model: str = "",
    ) -> None:
        self.ws = workspace
        self.git = Git(workspace.root)
        self.ledger = Ledger(workspace.ledger_dir)
        self.store = Store(workspace.artifacts_dir)
        self.cache = Cache(
            workspace.cache_dir,
            self.store,
            enabled=bool(workspace.setting("cache.enabled", True)) and not no_cache,
            store_failures=bool(workspace.setting("cache.store_failures", False)),
        )
        self.base = base
        self.advisory_only = advisory_only
        self.approve = set(approve)
        self.keep_worktree = keep_worktree
        self.limits = limits_from_config(workspace.config)
        self.corpus = Corpus(workspace.corpus_path())
        self.actor: Actor = resolve_actor(workspace.root, declared_model=declared_model)

    # ---- helpers --------------------------------------------------------- #

    def _pack(self) -> Pack:
        return load_pack(self.ws.policy_dir, str(self.ws.setting("policy.pack", "default")))

    def _has_approval(self, token: str) -> bool:
        """Scoped to this token, not to "some approval exists".

        The ledger is append-only, so every approval ever granted is still in it. An
        unscoped query would let last week's sign-off authorise today's code.
        """
        for record in self.ledger.read_all():
            if record.type == APPROVAL_RECORDED and record.body.get("token") == token:
                return True
        return False

    def record_approval(self, token: str, *, phase: str, run_id: str, note: str = "") -> None:
        self.ledger.append(
            APPROVAL_RECORDED,
            {
                "token": token,
                "phase": phase,
                "actor": self.actor.to_json(),
                "note": note,
            },
            run_id=run_id,
            stage=phase,
        )

    # ---- the run --------------------------------------------------------- #

    def run(self, plan: Plan) -> RunResult:
        if not self.git.is_repo():
            raise UsageError(f"{self.ws.root} is not a git repository")

        pack = self._pack()
        drift = pack.drift(self.corpus)
        run_id = new_run_id()
        run_dir = ensure_dir(self.ws.run_dir(run_id))
        sandbox, backend_note = select_sandbox(
            str(self.ws.setting("execution.backend", "auto")),
            str(self.ws.setting("execution.image", "python:3.11-slim")),
        )

        result = RunResult(
            run_id=run_id,
            status="running",
            plan=plan.name,
            snapshot=None,
            run_dir=run_dir,
            backend_note=backend_note,
            drift=drift,
        )
        started = utc_now()

        self.ledger.append(
            RUN_STARTED,
            {
                "harness": __version__,
                "plan": {"name": plan.name, "digest": plan.digest, "source": plan.source},
                "policy": {"pack": pack.name, "digest": pack.digest, "drift": len(drift)},
                "actor": self.actor.to_json(),
                "scm": self.git.facts(self.base),
                "execution": {"backend": sandbox.name, "resolution": backend_note},
            },
            run_id=run_id,
        )

        snapshot = self.git.snapshot(
            run_id,
            message=f"awesome-harness snapshot for run {run_id} ({plan.name})",
            author=f"{self.actor.name or 'awesome-harness'} <{self.actor.email or 'harness@localhost'}>",
            tmp_dir=self.ws.tmp_dir,
        )
        result.snapshot = snapshot
        self.ledger.append(
            SNAPSHOT_CREATED,
            {
                "tree": snapshot.tree,
                "commit": snapshot.commit,
                "ref": snapshot.ref,
                "parent": snapshot.parent,
                "changed": list(snapshot.changed[:200]),
                "changed_count": len(snapshot.changed),
            },
            run_id=run_id,
        )

        worktree = run_dir / "work"
        self.git.add_worktree(snapshot.commit, worktree)
        gate_result = None
        try:
            for phase in plan.phases:
                self.ledger.append(
                    STAGE_STARTED,
                    {"stage": phase.name, "steps": [s.id for s in phase.steps], "gate": phase.gate},
                    run_id=run_id,
                    stage=phase.name,
                )

                if phase.approval:
                    token = approval_token(
                        plan_digest=plan.digest,
                        phase=phase.name,
                        tree=snapshot.tree,
                        pack_digest=pack.digest,
                    )
                    if phase.name in self.approve or "*" in self.approve:
                        self.record_approval(token, phase=phase.name, run_id=run_id, note="approved on this run")
                    elif not self._has_approval(token):
                        result.status = "awaiting-approval"
                        raise ApprovalRequired(
                            f"phase {phase.name!r} requires approval for tree {snapshot.tree[:12]}",
                            hint=(
                                f"record it with: awesome-harness approve {phase.name} "
                                f"--token {token}\n  (or re-run with --approve {phase.name})"
                            ),
                        )

                for step in phase.steps:
                    outcome = self._run_step(
                        step,
                        phase=phase,
                        run_id=run_id,
                        run_dir=run_dir,
                        worktree=worktree,
                        sandbox=sandbox,
                        pack=pack,
                        snapshot=snapshot,
                    )
                    result.steps.append(outcome)
                    if outcome.exit_code != 0 and not step.allow_failure:
                        result.status = "failed"
                        raise ExecutionError(
                            f"step {step.id!r} in phase {phase.name!r} exited {outcome.exit_code}",
                            hint=f"logs: {run_dir / (step.id + '.stderr')}",
                        )

                if phase.gate:
                    gate_result = self._run_gate(
                        pack=pack, phase=phase, run_id=run_id, run_dir=run_dir
                    )
                    result.gate = gate_summary(gate_result)
                    if gate_result.verdict == "fail" and not self.advisory_only:
                        result.status = "gate-failed"
                        raise GateFailed(
                            f"policy gate failed in phase {phase.name!r}: "
                            f"{len(gate_result.blocking)} blocking finding(s)",
                            hint=f"report: {run_dir / 'gate.json'}",
                        )

                self.ledger.append(
                    STAGE_FINISHED, {"stage": phase.name, "status": "ok"}, run_id=run_id, stage=phase.name
                )

            result.status = "passed"
            return result
        finally:
            # The attestation is written whatever the outcome. A run that failed its
            # gate is exactly the run whose provenance someone will want to read, and
            # withholding it would leave the failure undocumented.
            try:
                self._finish(
                    plan=plan,
                    pack=pack,
                    result=result,
                    run_id=run_id,
                    run_dir=run_dir,
                    snapshot=snapshot,
                    sandbox_name=sandbox.name,
                    backend_note=backend_note,
                    started=started,
                    gate_result=gate_result,
                )
            finally:
                if not self.keep_worktree:
                    self.git.remove_worktree(worktree)
                    shutil.rmtree(worktree, ignore_errors=True)

    # ---- steps ----------------------------------------------------------- #

    def _run_step(
        self,
        step: Step,
        *,
        phase: Phase,
        run_id: str,
        run_dir: Path,
        worktree: Path,
        sandbox: Any,
        pack: Pack,
        snapshot: Snapshot,
    ) -> StepOutcome:
        env = build_env(
            allow=list(self.ws.setting("execution.env_allow", [])),
            fixed=dict(self.ws.setting("execution.env_fixed", {})),
            step_env=step.env,
            home=ensure_dir(run_dir / "home"),
        )
        isolation = sandbox.isolation(step, self.limits)
        key_inputs = self.cache.key_inputs(
            step,
            # Inputs are digested from the *snapshot worktree*, not the live tree, so
            # an edit made while the run is in flight cannot change the key underneath
            # the execution it describes.
            input_digests=digest_tree(worktree, _expand_inputs(worktree, step.inputs)),
            tool_digests=tool_fingerprints(step.tools, cwd=worktree, env=env),
            env_digests=env_fingerprint(env),
            policy_pack_digest=pack.digest,
            isolation=isolation,
        )
        lookup = self.cache.lookup(step, key_inputs)

        if lookup.hit and lookup.entry is not None:
            entry = lookup.entry
            manifest = Manifest(
                run_id=run_id,
                step=step.id,
                source_tree=snapshot.tree,
                source_commit=snapshot.commit,
                artifacts=list(entry.outputs),
            )
            # Restored, then re-verified against the digests the entry recorded.
            self.store.materialize(manifest, worktree, verify=True)
            self.ledger.append(
                CACHE_HIT,
                {
                    "step": step.id,
                    "key": lookup.key,
                    "outputs": [a.digest for a in entry.outputs],
                    "saved_ms": entry.duration_ms,
                },
                run_id=run_id,
                stage=phase.name,
            )
            return StepOutcome(
                step=step.id,
                exit_code=entry.exit_code,
                duration_ms=0,
                cached=True,
                backend=entry.backend,
                cache_key=lookup.key,
                outputs=list(entry.outputs),
                note=f"replayed from cache (originally {entry.duration_ms} ms on {entry.backend})",
            )

        self.ledger.append(
            CACHE_MISS,
            {"step": step.id, "key": lookup.key, "reason": lookup.reason, "why": lookup.explanation[:8]},
            run_id=run_id,
            stage=phase.name,
        )
        self.cache.record_key(step.id, key_inputs, lookup.key)

        self.ledger.append(
            STEP_STARTED,
            {**ledger_body(step, env), "isolation": isolation},
            run_id=run_id,
            stage=phase.name,
        )
        raw = sandbox.execute(step, workdir=worktree, env=env, limits=self.limits, run_dir=run_dir)

        outputs: list[Artifact] = []
        for output, path in collect_outputs(step, worktree):
            name = path.relative_to(worktree).as_posix() if path.exists() else output.path
            artifact = self.store.put_file(
                path, name=name, allow_empty=output.allow_empty
            )
            outputs.append(artifact)
            self.ledger.append(
                ARTIFACT_PUBLISHED,
                {"step": step.id, "name": artifact.name, "digest": artifact.digest, "size": artifact.size},
                run_id=run_id,
                stage=phase.name,
            )

        log_digests: dict[str, str | None] = {}
        for stream in ("stdout", "stderr"):
            path = run_dir / f"{step.id}.{stream}"
            log_digests[stream] = digest_file(path) if path.is_file() and path.stat().st_size else None

        self.ledger.append(
            STEP_FINISHED,
            {
                "step": step.id,
                "exit_code": raw.exit_code,
                "duration_ms": raw.duration_ms,
                "backend": sandbox.name,
                "truncated": raw.truncated,
                "redactions": raw.redactions,
                "stdout_digest": log_digests["stdout"],
                "stderr_digest": log_digests["stderr"],
                "outputs": [a.digest for a in outputs],
            },
            run_id=run_id,
            stage=phase.name,
        )

        self.cache.save(
            Entry(
                key=lookup.key,
                step=step.id,
                exit_code=raw.exit_code,
                duration_ms=raw.duration_ms,
                outputs=outputs,
                stdout_digest=log_digests["stdout"],
                stderr_digest=log_digests["stderr"],
                backend=sandbox.name,
            ),
            key_inputs,
        )
        return StepOutcome(
            step=step.id,
            exit_code=raw.exit_code,
            duration_ms=raw.duration_ms,
            cached=False,
            backend=sandbox.name,
            cache_key=lookup.key,
            outputs=outputs,
            redactions=raw.redactions,
            note="" if lookup.eligible else f"not cached: {lookup.reason}",
        )

    # ---- gate ------------------------------------------------------------ #

    def _run_gate(self, *, pack: Pack, phase: Phase, run_id: str, run_dir: Path) -> Any:
        ctx = build_context(self.git, self.ws.root, self.base)
        waivers = Waivers.load(self.ws.waivers_path)
        result = evaluate_gate(pack, ctx, waivers=waivers, threshold=str(self.ws.setting("policy.threshold", "error")))

        bundle, slugs, notes = advisory_bundle(pack, self.corpus, ctx.files)
        result.advisory_slugs = slugs
        result.notes.extend(notes)

        atomic_write_json(run_dir / "gate.json", result.to_json())
        atomic_write_bytes(run_dir / "review-context.md", bundle.encode("utf-8"))

        self.ledger.append(
            GATE_EVALUATED,
            {
                **gate_summary(result),
                "counts": result.counts,
                "files_examined": result.files_examined,
                "checks_run": result.checks_run,
                "advisory_delivered": len(slugs),
                "top": [f.to_json() for f in result.findings[:20]],
            },
            run_id=run_id,
            stage=phase.name,
        )
        return result

    # ---- attestation ----------------------------------------------------- #

    def _finish(
        self,
        *,
        plan: Plan,
        pack: Pack,
        result: RunResult,
        run_id: str,
        run_dir: Path,
        snapshot: Snapshot,
        sandbox_name: str,
        backend_note: str,
        started: str,
        gate_result: Any,
    ) -> None:
        artifacts: list[Artifact] = [a for outcome in result.steps for a in outcome.outputs]
        manifest = Manifest(
            run_id=run_id,
            step="run",
            source_tree=snapshot.tree,
            source_commit=snapshot.commit,
            artifacts=artifacts,
        )
        atomic_write_json(run_dir / "manifest.json", manifest.to_json())

        subjects = [
            {"name": a.name, "digest": {"sha256": a.digest.split(":", 1)[1]}} for a in artifacts
        ]
        subjects.append(
            {"name": "run-manifest", "digest": {"sha256": manifest.digest.split(":", 1)[1]}}
        )

        head = self.ledger.head()
        records = len(self.ledger.read_all())
        statement = build_statement(
            run_id=run_id,
            subjects=subjects,
            plan={
                "plan": plan.name,
                "planDigest": plan.digest,
                "source": plan.source,
                "base": self.base or "",
                "advisoryOnly": self.advisory_only,
            },
            actor=self.actor,
            scm={
                **self.git.facts(self.base),
                "snapshot_commit": snapshot.commit,
                "snapshot_tree": snapshot.tree,
                "snapshot_ref": snapshot.ref,
            },
            policy={
                "pack": pack.name,
                "packDigest": pack.digest,
                "threshold": pack.threshold,
                "machineRules": len(pack.machine_rules),
                "advisoryRules": len(pack.advisory_rules),
                "corpusDrift": result.drift,
                "verdict": (gate_result.verdict if gate_result else "not-evaluated"),
                "findingsDigest": (gate_result.findings_digest if gate_result else ""),
                "advisoryDelivered": (gate_result.advisory_slugs if gate_result else []),
            },
            steps=[s.to_json() for s in result.steps],
            isolation={"backend": sandbox_name, "resolution": backend_note},
            ledger_head=head,
            started=started,
            finished=utc_now(),
        )
        # Record count alongside the head: a head digest on its own can be reproduced
        # by truncating the ledger and re-chaining from an earlier record.
        statement["predicate"]["runDetails"]["metadata"]["ledgerRecords"] = records

        payload = statement_bytes(statement)
        signer = Signer(
            key=str(self.ws.setting("identity.key", "")),
            namespace=str(self.ws.setting("identity.namespace", "awesome-harness")),
        )
        if str(self.ws.setting("identity.signer", "ssh")) == "ssh":
            envelope = signer.sign(payload, scratch=self.ws.tmp_dir)
        else:
            envelope = Envelope(payload=payload, unsigned_reason="identity.signer is not 'ssh'")
        path = ensure_dir(self.ws.attestations_dir) / f"{run_id}.json"
        atomic_write_json(path, envelope.to_json())
        result.attestation = path
        result.signature = "signed" if envelope.signatures else "unsigned"

        self.ledger.append(
            ATTESTATION_CREATED,
            {
                "path": str(path.relative_to(self.ws.root)),
                "payload_digest": envelope.digest,
                "signature": result.signature,
                "reason": envelope.unsigned_reason,
                "subjects": len(subjects),
                "ledger_records": records,
            },
            run_id=run_id,
        )
        self.ledger.append(
            RUN_FINISHED,
            {
                "status": result.status,
                "steps": len(result.steps),
                "cached": sum(1 for s in result.steps if s.cached),
                "gate": result.gate,
            },
            run_id=run_id,
        )
        atomic_write_json(run_dir / "run.json", result.to_json())


def _expand_inputs(root: Path, patterns: Iterable[str]) -> list[str]:
    """Resolve input globs to repository-relative paths inside the snapshot.

    Sorted and de-duplicated, because this list is hashed. A glob matching nothing
    contributes nothing rather than raising: the file may legitimately not exist yet,
    and `digest_tree` records that absence as its own value.
    """
    found: set[str] = set()
    for pattern in patterns:
        if any(ch in pattern for ch in "*?["):
            for path in root.glob(pattern):
                if path.is_file():
                    found.add(path.relative_to(root).as_posix())
        else:
            found.add(pattern)
    return sorted(found)
