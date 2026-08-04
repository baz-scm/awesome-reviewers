"""Pillar 1 — the ledger's tamper evidence and the snapshot's immutability.

The tamper matrix is the point of this file. A hash chain nobody has tried to break
is a hash chain nobody knows works, so each test mutates the ledger in a specific,
plausible way and asserts that `verify` localises it.
"""

from __future__ import annotations

import json
import unittest

from awesome_harness.digest import ZERO
from awesome_harness.errors import IntegrityError, UsageError
from awesome_harness.ledger import (
    GATE_EVALUATED,
    STAGE_STARTED,
    STEP_FINISHED,
    Ledger,
)
from awesome_harness.scm import Git

from .support import TempRepo, git


class TestLedgerChain(TempRepo):
    def setUp(self) -> None:
        super().setUp()
        self.ledger = Ledger(self.ws.ledger_dir)

    def _seed(self, count: int = 5) -> None:
        for index in range(count):
            self.ledger.append(
                STEP_FINISHED, {"step": f"s{index}", "exit_code": 0}, run_id="r1", stage="build"
            )

    def test_genesis_links_to_the_zero_sentinel(self) -> None:
        record = self.ledger.append(STEP_FINISHED, {"step": "first"}, run_id="r1")
        self.assertEqual(record.prev, ZERO)
        self.assertEqual(record.seq, 1)

    def test_each_record_links_to_its_predecessor(self) -> None:
        first = self.ledger.append(STEP_FINISHED, {"step": "a"}, run_id="r1")
        second = self.ledger.append(STEP_FINISHED, {"step": "b"}, run_id="r1")
        self.assertEqual(second.prev, first.digest)
        self.assertEqual(second.seq, 2)

    def test_clean_chain_verifies(self) -> None:
        self._seed()
        result = self.ledger.verify()
        self.assertTrue(result.ok, result.reason)
        self.assertEqual(result.count, 5)

    def test_editing_a_middle_record_is_detected_at_that_record(self) -> None:
        self._seed()
        lines = self.ledger.path.read_text(encoding="utf-8").strip().split("\n")
        record = json.loads(lines[2])
        record["body"]["exit_code"] = 1  # the edit somebody would actually make
        lines[2] = json.dumps(record, separators=(",", ":"), sort_keys=True)
        self.ledger.path.write_text("\n".join(lines) + "\n", encoding="utf-8")

        result = self.ledger.verify()
        self.assertFalse(result.ok)
        self.assertEqual(result.broken_at, 3)
        self.assertIn("was modified", result.reason or "")

    def test_removing_a_record_is_detected_as_a_sequence_jump(self) -> None:
        self._seed()
        lines = self.ledger.path.read_text(encoding="utf-8").strip().split("\n")
        del lines[2]
        self.ledger.path.write_text("\n".join(lines) + "\n", encoding="utf-8")

        result = self.ledger.verify()
        self.assertFalse(result.ok)
        self.assertEqual(result.broken_at, 4)
        self.assertIn("sequence jumped", result.reason or "")

    def test_reordering_records_is_detected(self) -> None:
        self._seed()
        lines = self.ledger.path.read_text(encoding="utf-8").strip().split("\n")
        lines[1], lines[2] = lines[2], lines[1]
        self.ledger.path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        self.assertFalse(self.ledger.verify().ok)

    def test_truncating_the_tail_leaves_a_valid_prefix(self) -> None:
        # Truncation alone is not detectable from the file: that is what the
        # attestation's recorded record *count* is for. The prefix must still verify,
        # so that a crash mid-run does not look like tampering.
        self._seed()
        lines = self.ledger.path.read_text(encoding="utf-8").strip().split("\n")
        self.ledger.path.write_text("\n".join(lines[:3]) + "\n", encoding="utf-8")
        result = self.ledger.verify()
        self.assertTrue(result.ok)
        self.assertEqual(result.count, 3)

    def test_a_torn_final_line_is_an_integrity_error_not_an_empty_read(self) -> None:
        self._seed(2)
        with open(self.ledger.path, "a", encoding="utf-8") as handle:
            handle.write('{"v":1,"seq":3,"at":"20')
        with self.assertRaises(IntegrityError):
            self.ledger.head()

    def test_unknown_record_type_is_refused_at_write_time(self) -> None:
        with self.assertRaises(UsageError):
            self.ledger.append("MADE_UP", {}, run_id="r1")


class TestStageScoping(TempRepo):
    """The re-entry semantics from aidlc-workflows-scoped-hash-based-idempotency."""

    def setUp(self) -> None:
        super().setUp()
        self.ledger = Ledger(self.ws.ledger_dir)

    def test_query_is_floored_at_the_latest_stage_start(self) -> None:
        self.ledger.append(STAGE_STARTED, {"stage": "build"}, run_id="r1", stage="build")
        self.ledger.append(GATE_EVALUATED, {"verdict": "fail"}, run_id="r1", stage="build")
        # Second attempt at the same stage in the same run.
        self.ledger.append(STAGE_STARTED, {"stage": "build"}, run_id="r1", stage="build")
        self.ledger.append(GATE_EVALUATED, {"verdict": "pass"}, run_id="r1", stage="build")

        scoped = self.ledger.since_stage_start("r1", "build", types=[GATE_EVALUATED])
        self.assertEqual(len(scoped), 1)
        self.assertEqual(scoped[0].body["verdict"], "pass")

        # Contrast: reading all of history would find the stale failure too, which is
        # exactly the bug the scoping prevents.
        everything = [r for r in self.ledger.read_all() if r.type == GATE_EVALUATED]
        self.assertEqual(len(everything), 2)

    def test_other_runs_do_not_leak_into_the_window(self) -> None:
        self.ledger.append(STAGE_STARTED, {"stage": "build"}, run_id="r1", stage="build")
        self.ledger.append(GATE_EVALUATED, {"verdict": "pass"}, run_id="r2", stage="build")
        self.assertEqual(self.ledger.since_stage_start("r1", "build"), [])


class TestSnapshots(TempRepo):
    def setUp(self) -> None:
        super().setUp()
        self.git = Git(self.root)

    def test_snapshot_captures_uncommitted_work_without_committing_it(self) -> None:
        head_before = self.git.head()
        branch_before = self.git.branch()
        self.write("new_file.py", "x = 1\n")

        snapshot = self.git.snapshot("run-1", message="test snapshot", tmp_dir=self.ws.tmp_dir)

        self.assertEqual(self.git.head(), head_before, "HEAD must not move")
        self.assertEqual(self.git.branch(), branch_before, "no branch may be created")
        self.assertIn("new_file.py", snapshot.changed)
        # The staging area is untouched: the snapshot went through a temp index.
        self.assertEqual(git(self.root, "diff", "--cached", "--name-only"), "")

    def test_snapshot_objects_are_real_and_reachable(self) -> None:
        self.write("thing.txt", "content\n")
        snapshot = self.git.snapshot("run-2", message="snap", tmp_dir=self.ws.tmp_dir)

        self.assertEqual(git(self.root, "cat-file", "-t", snapshot.commit), "commit")
        self.assertEqual(git(self.root, "cat-file", "-t", snapshot.tree), "tree")
        # Anchored by a ref, so garbage collection cannot take it.
        self.assertEqual(git(self.root, "rev-parse", snapshot.ref), snapshot.commit)
        self.assertIn("thing.txt", git(self.root, "ls-tree", "-r", "--name-only", snapshot.tree))

    def test_identical_content_yields_the_identical_tree(self) -> None:
        self.write("same.txt", "stable\n")
        first = self.git.snapshot("run-a", message="a", tmp_dir=self.ws.tmp_dir)
        second = self.git.snapshot("run-b", message="b", tmp_dir=self.ws.tmp_dir)
        self.assertEqual(first.tree, second.tree, "content identity must be reproducible")

    def test_gitignored_files_stay_out_of_the_snapshot(self) -> None:
        self.write(".gitignore", "build/\n")
        self.write("build/artifact.bin", "derived\n")
        self.write("source.txt", "real\n")
        snapshot = self.git.snapshot("run-3", message="snap", tmp_dir=self.ws.tmp_dir)
        listing = git(self.root, "ls-tree", "-r", "--name-only", snapshot.tree)
        self.assertIn("source.txt", listing)
        self.assertNotIn("build/artifact.bin", listing)


class TestChangeScoping(TempRepo):
    def setUp(self) -> None:
        super().setUp()
        self.git = Git(self.root)

    def test_added_lines_only(self) -> None:
        self.write("mod.py", "a = 1\nb = 2\nc = 3\n")
        self.commit("base")
        self.write("mod.py", "a = 1\nb = 22\nc = 3\nd = 4\n")

        added = {(h.path, h.text) for h in self.git.added_lines()}
        self.assertIn(("mod.py", "b = 22"), added)
        self.assertIn(("mod.py", "d = 4"), added)
        self.assertNotIn(("mod.py", "a = 1"), added)

    def test_untracked_files_are_fully_in_scope(self) -> None:
        self.write("brand_new.py", "import os\nx = 1\n")
        hunks = [h for h in self.git.added_lines() if h.path == "brand_new.py"]
        self.assertEqual([h.text for h in hunks], ["import os", "x = 1"])
        self.assertEqual([h.line for h in hunks], [1, 2])

    def test_deletions_are_not_reported_as_changed_files(self) -> None:
        self.write("gone.py", "x = 1\n")
        self.commit("add")
        (self.root / "gone.py").unlink()
        self.assertNotIn("gone.py", self.git.changed_files())


if __name__ == "__main__":
    unittest.main()
