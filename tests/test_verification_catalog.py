"""Behavioral checks for provenance, separation and safe catalog regeneration."""

from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

import build_verification as catalog


SHA = "a" * 40


def manifest() -> dict:
    """Synthetic test data, never part of the published source corpus."""
    return {
        "schema_version": 1,
        "repository": "example/project",
        "commit_sha": SHA,
        "default_branch": "main",
        "scanned_at": "2026-11-01T09:00:00Z",
        "coverage": {
            "tree_complete": True, "files_considered": 12,
            "candidate_files": 3, "files_fetched": 2, "files_skipped": 1,
            "limitations": ["One candidate exceeded the scan budget."],
        },
        "methods": [{
            "id": "example--project--property_based_testing",
            "method": "property_based_testing",
            "title": "Property-based testing",
            "category": "testing",
            "summary": "Synthetic check for catalog tests.",
            "tools": ["proptest"],
            "commands": ["cargo test"],
            "status": "ci_configured",
            "evidence": [{
                "path": ".github/workflows/check.yml",
                "start_line": 10, "end_line": 11,
                "excerpt": "run: cargo test\nworking-directory: crates/example",
                "url": f"https://github.com/example/project/blob/{SHA}/.github/workflows/check.yml#L10-L11",
                "kind": "ci_configured",
                "conditions": ["github.event_name == 'pull_request'"],
                "working_directory": "crates/example",
                "environment": {"PROPTEST_CASES": "64"},
            }],
        }],
    }


def save(root: Path, value: dict) -> Path:
    folder = root / "_verification"
    folder.mkdir(exist_ok=True)
    path = folder / "example--project.json"
    path.write_text(json.dumps(value), encoding="utf-8")
    return path


class EvidenceValidation(unittest.TestCase):
    def test_rejects_mutable_branch_source_links(self):
        value = manifest()
        value["methods"][0]["evidence"][0]["url"] = value["methods"][0]["evidence"][0]["url"].replace(SHA, "main")
        with self.assertRaisesRegex(ValueError, "exact repository, commit"):
            catalog.validate_manifest(value)

    def test_rejects_evidence_from_a_different_repository(self):
        value = manifest()
        value["methods"][0]["evidence"][0]["url"] = value["methods"][0]["evidence"][0]["url"].replace("example/project", "other/project")
        with self.assertRaises(ValueError):
            catalog.validate_manifest(value)

    def test_rejects_line_range_and_link_disagreement(self):
        value = manifest()
        value["methods"][0]["evidence"][0]["start_line"] = 9
        with self.assertRaisesRegex(ValueError, "line range"):
            catalog.validate_manifest(value)

    def test_rejects_truncated_excerpt_for_a_larger_source_range(self):
        value = manifest()
        value["methods"][0]["evidence"][0]["excerpt"] = "run: cargo test"
        with self.assertRaisesRegex(ValueError, "complete linked line range"):
            catalog.validate_manifest(value)

    def test_rejects_inconsistent_scan_coverage(self):
        for change in ({"candidate_files": 13}, {"files_fetched": 1}):
            with self.subTest(change=change):
                value = manifest()
                value["coverage"].update(change)
                with self.assertRaises(ValueError):
                    catalog.validate_manifest(value)

    def test_rejects_a_claim_without_evidence(self):
        value = manifest()
        value["methods"][0]["evidence"] = []
        with self.assertRaisesRegex(ValueError, "evidence is required"):
            catalog.validate_manifest(value)

    def test_rejects_ci_claim_with_only_implementation_evidence(self):
        value = manifest()
        value["methods"][0]["evidence"][0]["kind"] = "implemented"
        with self.assertRaisesRegex(ValueError, "matching source evidence"):
            catalog.validate_manifest(value)

    def test_agent_instructions_do_not_establish_a_method(self):
        value = manifest()
        evidence = value["methods"][0]["evidence"][0]
        evidence["path"] = "skills/checks/SKILL.md"
        evidence["url"] = f"https://github.com/example/project/blob/{SHA}/skills/checks/SKILL.md#L10-L11"
        with self.assertRaisesRegex(ValueError, "instruction files"):
            catalog.validate_manifest(value)

    def test_rejects_method_id_that_can_escape_output_directory(self):
        value = manifest()
        value["methods"][0]["id"] = "example--project--../../outside"
        with self.assertRaises(ValueError):
            catalog.validate_manifest(value)

    def test_rejects_naive_scan_timestamp(self):
        value = manifest()
        value["scanned_at"] = "2026-11-01T09:00:00"
        with self.assertRaisesRegex(ValueError, "timezone"):
            catalog.validate_manifest(value)

    def test_preserves_job_context_without_mutating_source(self):
        value = manifest()
        original = copy.deepcopy(value)
        validated = catalog.validate_manifest(value)
        evidence = validated["methods"][0]["evidence"][0]
        self.assertEqual(evidence["conditions"], ["github.event_name == 'pull_request'"])
        self.assertEqual(evidence["working_directory"], "crates/example")
        self.assertEqual(evidence["environment"], {"PROPTEST_CASES": "64"})
        self.assertEqual(value, original)


class CatalogPublication(unittest.TestCase):
    def test_keeps_legacy_data_separate_and_preserves_existing_raw_files(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "_reviewers").mkdir()
            (root / "_reviewers" / "old.md").write_text("Use property testing.", encoding="utf-8")
            (root / "raw").mkdir()
            legacy = root / "raw" / "legacy.md"
            legacy.write_text("Original instruction.", encoding="utf-8")
            output = catalog.build(root)
            self.assertEqual(output["total"], 0)
            self.assertEqual(output["repository_count"], 0)
            self.assertEqual(legacy.read_text(), "Original instruction.")

    def test_empty_scan_is_visible_as_inspected_without_inventing_methods(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            value = manifest()
            value["methods"] = []
            save(root, value)
            output = catalog.build(root)
            self.assertEqual(output["total"], 0)
            self.assertEqual(output["repository_count"], 1)
            self.assertEqual(output["repositories"][0]["coverage"]["files_skipped"], 1)

    def test_removes_stale_method_pages_and_raw_records(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            value = manifest()
            save(root, value)
            catalog.build(root)
            method_id = value["methods"][0]["id"]
            page = root / "methods" / method_id / "index.html"
            raw = root / "raw" / "verification" / f"{method_id}.json"
            self.assertTrue(page.exists())
            self.assertTrue(raw.exists())
            value["methods"] = []
            save(root, value)
            catalog.build(root)
            self.assertFalse(page.exists())
            self.assertFalse(raw.exists())

    def test_invalid_scan_does_not_replace_previously_built_catalog(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            value = manifest()
            save(root, value)
            catalog.build(root)
            index = root / "raw" / "verification" / "index.json"
            before = index.read_bytes()
            value["methods"][0]["evidence"] = []
            save(root, value)
            with self.assertRaises(ValueError):
                catalog.build(root)
            self.assertEqual(index.read_bytes(), before)

    def test_multiple_manifests_for_one_repository_are_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = save(root, manifest())
            (source.parent / "duplicate.json").write_bytes(source.read_bytes())
            with self.assertRaisesRegex(ValueError, "duplicate repository"):
                catalog.build(root)

    def test_records_commands_as_text_without_running_them(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            marker = root / "should-not-exist"
            value = manifest()
            value["methods"][0]["commands"] = [f"touch {marker}"]
            save(root, value)
            output = catalog.build(root)
            self.assertFalse(marker.exists())
            record = root / output["entries"][0]["raw_markdown"].lstrip("/")
            self.assertIn(str(marker), record.read_text())

    def test_markdown_keeps_source_fences_and_conditions_intact(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            value = manifest()
            value["methods"][0]["evidence"][0]["excerpt"] = "run: echo '\x60\x60\x60'\nname: check"
            save(root, value)
            output = catalog.build(root)
            record = root / output["entries"][0]["raw_markdown"].lstrip("/")
            contents = record.read_text()
            self.assertFalse(contents.startswith("---"))
            self.assertIn("github.event_name == 'pull_request'", contents)
            self.assertIn("PROPTEST_CASES", contents)
            self.assertIn("\x60\x60\x60\x60\nrun:", contents)


if __name__ == "__main__":
    unittest.main()
