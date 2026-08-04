"""Pillars 3 and 4 — bundle determinism, store integrity, and cache key discipline.

Two claims are load-bearing and therefore tested adversarially:

  a bundle is byte-identical across machines — so the test varies umask, mtimes and
  member permissions and demands the same digest

  a cache key is a function of content — so the test changes each input in turn and
  demands a different key, then changes things that must *not* matter and demands
  the same one
"""

from __future__ import annotations

import os
import tarfile
import time
import unittest
from dataclasses import replace
from pathlib import Path

from awesome_harness.artifacts import EmptyArtifact, Manifest, Store
from awesome_harness.cache import Cache, Entry, isolation_keyable, platform_identity
from awesome_harness.digest import digest_file
from awesome_harness.errors import CacheCollision, IntegrityError
from awesome_harness.execution import Step
from awesome_harness.paths import PathEscape

from .support import TempRepo


class TestStore(TempRepo):
    def setUp(self) -> None:
        super().setUp()
        self.store = Store(self.ws.artifacts_dir)
        self.work = self.root / "work"
        self.work.mkdir(exist_ok=True)

    def _file(self, name: str, content: bytes) -> Path:
        path = self.work / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
        return path

    def test_put_is_idempotent_and_content_addressed(self) -> None:
        first = self.store.put_file(self._file("a.txt", b"same"), name="a.txt")
        second = self.store.put_file(self._file("b.txt", b"same"), name="b.txt")
        self.assertEqual(first.digest, second.digest)
        self.assertEqual(self.store.size()[0], 1, "identical content stores one blob")

    def test_zero_byte_output_is_refused_unless_declared(self) -> None:
        empty = self._file("nothing.log", b"")
        with self.assertRaises(EmptyArtifact):
            self.store.put_file(empty, name="nothing.log")
        allowed = self.store.put_file(empty, name="nothing.log", allow_empty=True)
        self.assertEqual(allowed.size, 0)

    def test_missing_declared_output_names_itself(self) -> None:
        with self.assertRaises(EmptyArtifact) as caught:
            self.store.put_file(self.work / "never-written.json", name="never-written.json")
        self.assertIn("never-written.json", str(caught.exception))

    def test_corrupted_blob_is_caught_on_read(self) -> None:
        artifact = self.store.put_file(self._file("c.txt", b"original"), name="c.txt")
        blob = self.store.blob_path(artifact.digest)
        blob.chmod(0o644)
        blob.write_bytes(b"tampered")
        with self.assertRaises(IntegrityError):
            self.store.read_bytes(artifact.digest)

    def test_materialize_confines_names(self) -> None:
        artifact = self.store.put_file(self._file("ok.txt", b"data"), name="ok.txt")
        manifest = Manifest(run_id="r", step="s", artifacts=[replace(artifact, name="../escape.txt")])
        with self.assertRaises(PathEscape):
            self.store.materialize(manifest, self.root / "out")

    def test_gc_defaults_to_dry_run(self) -> None:
        artifact = self.store.put_file(self._file("d.txt", b"data"), name="d.txt")
        count, freed = self.store.gc([])
        self.assertEqual(count, 1)
        self.assertGreater(freed, 0)
        self.assertTrue(self.store.has(artifact.digest), "dry run must not delete")
        self.store.gc([], dry_run=False)
        self.assertFalse(self.store.has(artifact.digest))

    def test_gc_keeps_referenced_blobs(self) -> None:
        keep = self.store.put_file(self._file("keep.txt", b"keep"), name="keep.txt")
        self.store.put_file(self._file("drop.txt", b"drop"), name="drop.txt")
        count, _ = self.store.gc([keep.digest], dry_run=False)
        self.assertEqual(count, 1)
        self.assertTrue(self.store.has(keep.digest))


class TestBundleDeterminism(TempRepo):
    def _build(self, *, umask: int, mtime: float, subdir: str) -> tuple[str, str]:
        previous = os.umask(umask)
        try:
            work = self.root / subdir / "work"
            work.mkdir(parents=True, exist_ok=True)
            for name, content in (
                ("a.txt", b"alpha\n"),
                ("nested/b.json", b'{"k":1}\n'),
                ("run.sh", b"#!/bin/sh\ntrue\n"),
            ):
                target = work / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(content)
                if name.endswith(".sh"):
                    target.chmod(0o755)
                os.utime(target, (mtime, mtime))
            store = Store(self.root / subdir / "store")
            manifest = Manifest(
                run_id="fixed",
                step="build",
                source_tree="0" * 40,
                source_commit="0" * 40,
                artifacts=[
                    store.put_file(work / n, name=n) for n in sorted(("a.txt", "nested/b.json", "run.sh"))
                ],
            )
            bundle = self.root / subdir / "out.tar"
            return store.export_bundle(manifest, bundle), manifest.digest
        finally:
            os.umask(previous)

    def test_identical_content_exports_identical_bytes(self) -> None:
        first_bundle, first_manifest = self._build(umask=0o022, mtime=1_000_000_000.0, subdir="one")
        second_bundle, second_manifest = self._build(umask=0o077, mtime=time.time(), subdir="two")
        self.assertEqual(first_manifest, second_manifest, "manifest digest must ignore the clock")
        self.assertEqual(first_bundle, second_bundle, "bundle bytes must ignore umask and mtime")

    def test_manifest_digest_excludes_created_timestamp(self) -> None:
        store = Store(self.ws.artifacts_dir)
        path = self.write("x.txt", "content\n")
        artifact = store.put_file(path, name="x.txt")
        early = Manifest(run_id="r", step="s", artifacts=[artifact], created="2020-01-01T00:00:00Z")
        late = Manifest(run_id="r", step="s", artifacts=[artifact], created="2030-01-01T00:00:00Z")
        self.assertEqual(early.digest, late.digest)

    def test_tar_members_carry_no_ambient_metadata(self) -> None:
        self._build(umask=0o022, mtime=1_700_000_000.0, subdir="meta")
        with tarfile.open(self.root / "meta" / "out.tar") as tar:
            members = tar.getmembers()
        self.assertTrue(members)
        for member in members:
            self.assertEqual(member.mtime, 0, member.name)
            self.assertEqual((member.uid, member.gid), (0, 0), member.name)
            self.assertEqual((member.uname, member.gname), ("", ""), member.name)
            self.assertIn(member.mode, (0o644, 0o755), member.name)
        self.assertEqual(members[0].name, "manifest.json", "manifest comes first, deterministically")


class TestBundleImport(TempRepo):
    def setUp(self) -> None:
        super().setUp()
        self.store = Store(self.ws.artifacts_dir)
        self.bundle = self.root / "bundle.tar"
        path = self.write("payload.txt", "real content\n")
        self.artifact = self.store.put_file(path, name="payload.txt")
        self.manifest = Manifest(run_id="r1", step="build", artifacts=[self.artifact])
        self.store.export_bundle(self.manifest, self.bundle)

    def test_round_trip_verifies(self) -> None:
        fresh = Store(self.root / "other-store")
        imported = fresh.import_bundle(self.bundle, scratch=self.ws.tmp_dir)
        self.assertEqual(imported.digest, self.manifest.digest)
        self.assertTrue(fresh.has(self.artifact.digest))

    def test_unlisted_member_is_rejected(self) -> None:
        # Smuggling: a member the manifest does not mention, in a bundle that would
        # otherwise verify.
        smuggled = self.root / "smuggled.tar"
        with tarfile.open(self.bundle) as source, tarfile.open(smuggled, "w") as target:
            for member in source.getmembers():
                extracted = source.extractfile(member)
                target.addfile(member, extracted)
            extra = tarfile.TarInfo(name="artifacts/extra.sh")
            payload = b"#!/bin/sh\necho pwned\n"
            extra.size = len(payload)
            import io

            target.addfile(extra, io.BytesIO(payload))
        with self.assertRaises(IntegrityError) as caught:
            Store(self.root / "s2").import_bundle(smuggled, scratch=self.ws.tmp_dir)
        self.assertIn("absent from its manifest", str(caught.exception))

    def test_manifest_digest_mismatch_is_rejected(self) -> None:
        # Editing the manifest inside the bundle breaks its self-digest.
        import io
        import json

        tampered = self.root / "tampered.tar"
        with tarfile.open(self.bundle) as source, tarfile.open(tampered, "w") as target:
            for member in source.getmembers():
                data = source.extractfile(member).read()  # type: ignore[union-attr]
                if member.name == "manifest.json":
                    payload = json.loads(data)
                    payload["artifacts"][0]["size"] = 999
                    data = json.dumps(payload).encode("utf-8")
                    member.size = len(data)
                target.addfile(member, io.BytesIO(data))
        with self.assertRaises(IntegrityError):
            Store(self.root / "s3").import_bundle(tampered, scratch=self.ws.tmp_dir)


class TestCacheKeys(TempRepo):
    def setUp(self) -> None:
        super().setUp()
        self.store = Store(self.ws.artifacts_dir)
        self.cache = Cache(self.ws.cache_dir, self.store)
        self.write("src/app.py", "print('v1')\n")
        self.step = Step(
            id="build",
            run=("python3", "-c", "print(1)"),
            inputs=("src/app.py",),
            tools=(),
        )

    def _inputs(self, **overrides):  # type: ignore[no-untyped-def]
        base = {
            "input_digests": {"src/app.py": digest_file(self.root / "src/app.py")},
            "tool_digests": {"python3 --version": "sha256:" + "a" * 64},
            "env_digests": {"PATH": "sha256:" + "b" * 64},
            "policy_pack_digest": "sha256:" + "c" * 64,
            "isolation": {"backend": "local"},
        }
        base.update(overrides)
        return self.cache.key_inputs(self.step, **base)

    def test_key_is_stable_for_identical_inputs(self) -> None:
        self.assertEqual(self._inputs().key(), self._inputs().key())

    def test_each_input_class_changes_the_key(self) -> None:
        baseline = self._inputs().key()
        cases = {
            "content": {"input_digests": {"src/app.py": "sha256:" + "f" * 64}},
            "tool version": {"tool_digests": {"python3 --version": "sha256:" + "e" * 64}},
            "environment": {"env_digests": {"PATH": "sha256:" + "d" * 64}},
            "policy pack": {"policy_pack_digest": "sha256:" + "9" * 64},
            "isolation": {"isolation": {"backend": "container", "image_digest": "sha256:x"}},
        }
        for label, override in cases.items():
            self.assertNotEqual(baseline, self._inputs(**override).key(), f"{label} must change the key")

    def test_command_change_changes_the_key(self) -> None:
        baseline = self._inputs().key()
        self.step = replace(self.step, run=("python3", "-c", "print(2)"))
        self.assertNotEqual(baseline, self._inputs().key())

    def test_key_ignores_things_that_must_not_matter(self) -> None:
        # If any of these entered the key, the hit rate would be permanently zero.
        first = self._inputs()
        second = self._inputs()
        self.assertEqual(first.key(), second.key())
        payload = first.to_json()
        for forbidden in ("run_id", "timestamp", "created", "hostname", "actor", "cwd_absolute", "ledger_head"):
            self.assertNotIn(forbidden, payload)

    def test_container_tag_without_a_digest_is_not_recorded_as_pinned(self) -> None:
        tagged = self._inputs(isolation={"backend": "container", "image": "python:3.11-slim"})
        self.assertIn("unpinned_image", tagged.isolation)
        self.assertNotIn("image_digest", tagged.isolation)

    def test_container_without_a_resolvable_digest_is_not_cacheable(self) -> None:
        # The failure this guards against: `docker run` on a missing image pulls it and
        # supplies the digest that was absent, so run 1 and run 2 compute different keys
        # from identical inputs and the cache misses forever while appearing to work.
        eligible, reason = Cache.eligibility(
            self.step, {"backend": "container", "unpinned_image": "python:3.11-slim"}
        )
        self.assertFalse(eligible)
        self.assertIn("no resolvable digest", reason)

    def test_container_with_a_resolved_digest_is_cacheable(self) -> None:
        eligible, _ = Cache.eligibility(
            self.step, {"backend": "container", "image_digest": "sha256:" + "a" * 64}
        )
        self.assertTrue(eligible)

    def test_lookup_refuses_an_unkeyable_isolation(self) -> None:
        lookup = self.cache.lookup(
            self.step, self._inputs(isolation={"backend": "container", "image": "python:3.11-slim"})
        )
        self.assertFalse(lookup.eligible)
        self.assertFalse(lookup.hit)
        self.assertIn("no resolvable digest", lookup.reason)

    def test_local_isolation_is_always_keyable(self) -> None:
        keyable, _ = isolation_keyable({"backend": "local"})
        self.assertTrue(keyable)

    def test_platform_identity_excludes_the_hostname(self) -> None:
        self.assertEqual(set(platform_identity()), {"system", "machine", "python"})

    def test_step_without_inputs_is_not_cacheable(self) -> None:
        eligible, reason = Cache.eligibility(Step(id="s", run=("true",)))
        self.assertFalse(eligible)
        self.assertIn("no inputs", reason)

    def test_network_step_is_not_cacheable(self) -> None:
        eligible, reason = Cache.eligibility(
            Step(id="s", run=("true",), inputs=("x",), allow_network=True)
        )
        self.assertFalse(eligible)
        self.assertIn("network", reason)

    def test_hit_and_miss_round_trip(self) -> None:
        inputs = self._inputs()
        self.assertFalse(self.cache.lookup(self.step, inputs).hit)
        artifact = self.store.put_file(self.write("out.bin", "built\n"), name="out.bin")
        self.cache.save(
            Entry(key=inputs.key(), step="build", exit_code=0, duration_ms=42, outputs=[artifact]),
            inputs,
        )
        lookup = self.cache.lookup(self.step, inputs)
        self.assertTrue(lookup.hit)
        self.assertEqual(lookup.entry.duration_ms, 42)  # type: ignore[union-attr]

    def test_failures_are_not_cached_by_default(self) -> None:
        inputs = self._inputs()
        stored = self.cache.save(Entry(key=inputs.key(), step="build", exit_code=1, duration_ms=1), inputs)
        self.assertFalse(stored)
        self.assertFalse(self.cache.lookup(self.step, inputs).hit)

    def test_evicted_blob_turns_a_hit_into_a_miss(self) -> None:
        inputs = self._inputs()
        artifact = self.store.put_file(self.write("out2.bin", "built\n"), name="out2.bin")
        self.cache.save(Entry(key=inputs.key(), step="build", exit_code=0, outputs=[artifact]), inputs)
        blob = self.store.blob_path(artifact.digest)
        blob.chmod(0o644)
        blob.unlink()
        lookup = self.cache.lookup(self.step, inputs)
        self.assertFalse(lookup.hit)
        self.assertIn("evicted", lookup.reason)

    def test_same_key_different_inputs_raises_loudly(self) -> None:
        import json

        inputs = self._inputs()
        self.cache.save(Entry(key=inputs.key(), step="build", exit_code=0), inputs)

        # Forge the condition the guard exists for: an entry sitting at this key's path
        # whose recorded inputs are not the inputs we just computed. In the wild this
        # is a non-deterministic field in the key function; here it is an edit.
        entry_path = self.cache.entry_path(inputs.key())
        payload = json.loads(entry_path.read_text(encoding="utf-8"))
        payload["key_inputs"]["inputs"]["src/app.py"] = "sha256:" + "1" * 64
        entry_path.write_text(json.dumps(payload), encoding="utf-8")

        with self.assertRaises(CacheCollision) as caught:
            self.cache.lookup(self.step, inputs)
        self.assertIn("src/app.py", str(caught.exception))

    def test_miss_is_explained_against_the_previous_key(self) -> None:
        first = self._inputs()
        self.cache.record_key("build", first, first.key())
        changed = self._inputs(input_digests={"src/app.py": "sha256:" + "7" * 64})
        lookup = self.cache.lookup(self.step, changed)
        self.assertFalse(lookup.hit)
        self.assertTrue(any("src/app.py" in note for note in lookup.explanation), lookup.explanation)

    def test_unreadable_entry_is_discarded_and_reported(self) -> None:
        inputs = self._inputs()
        path = self.cache.entry_path(inputs.key())
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("{not json", encoding="utf-8")
        lookup = self.cache.lookup(self.step, inputs)
        self.assertFalse(lookup.hit)
        self.assertIn("unreadable", lookup.reason)
        self.assertFalse(path.exists(), "a corrupt entry is removed, not left to fail forever")


if __name__ == "__main__":
    unittest.main()
