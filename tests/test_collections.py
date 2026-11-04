"""Front matter is the data: every reviewer and verification technique must carry
the fields the site renders and filters on. Jekyll fails the build on bad YAML;
this checks the shape and the cross-file rules Jekyll cannot."""
import re
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
FRONT_MATTER = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
TECHNIQUE_ID = re.compile(r"V\d{4}$")
SUBTECHNIQUE_ID = re.compile(r"V\d{4}\.\d{3}$")


def load(path: Path) -> dict:
    match = FRONT_MATTER.match(path.read_text(encoding="utf8"))
    if not match:
        raise AssertionError(f"{path.name}: no front matter")
    try:
        return yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError as error:
        raise AssertionError(f"{path.name}: invalid YAML: {error}") from error


class ReviewerTests(unittest.TestCase):
    REQUIRED = ("title", "description", "repository", "label", "language", "comments_count", "repository_stars")

    @classmethod
    def setUpClass(cls):
        cls.entries = {p.stem: load(p) for p in sorted((ROOT / "_reviewers").glob("*.md"))}

    def test_every_reviewer_has_required_fields(self):
        for slug, data in self.entries.items():
            for key in self.REQUIRED:
                self.assertIn(key, data, f"{slug}: missing {key}")
                self.assertNotEqual(str(data[key]).strip(), "", f"{slug}: empty {key}")

    def test_counts_are_integers(self):
        for slug, data in self.entries.items():
            self.assertIsInstance(data["comments_count"], int, f"{slug}: comments_count")
            self.assertIsInstance(data["repository_stars"], int, f"{slug}: repository_stars")

    def test_repository_is_owner_slash_name(self):
        for slug, data in self.entries.items():
            self.assertRegex(data["repository"], r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$", slug)


class VerificationTests(unittest.TestCase):
    """Each sub-technique is one verification entry, under one technique and tactic."""

    @classmethod
    def setUpClass(cls):
        cls.entries = {p.stem: load(p) for p in sorted((ROOT / "_verification").glob("*.md"))}
        cls.techniques = {p.stem: load(p) for p in sorted((ROOT / "_techniques").glob("*.md"))}

    def test_ids_are_unique_and_well_formed(self):
        ids = [data["code"] for data in self.entries.values()]
        self.assertEqual(len(ids), len(set(ids)), "sub-technique ids must be unique")
        for slug, data in self.entries.items():
            self.assertRegex(data["code"], SUBTECHNIQUE_ID, slug)

    def test_each_sub_sits_under_its_technique(self):
        technique_ids = {data["code"] for data in self.techniques.values()}
        for slug, data in self.entries.items():
            self.assertIn(data["technique_id"], technique_ids, slug)
            self.assertTrue(data["code"].startswith(data["technique_id"] + "."), f"{slug}: {data['code']}")

    def test_every_technique_lists_its_subs(self):
        listed = {s["id"] for data in self.techniques.values() for s in data["subtechniques"]}
        self.assertEqual(listed, {data["code"] for data in self.entries.values()})

    def test_every_sub_has_craft_and_signals(self):
        for slug, data in self.entries.items():
            self.assertTrue(data.get("craft"), f"{slug}: no craft steps")
            self.assertTrue(data.get("reverse"), f"{slug}: no signals")
            self.assertTrue(data.get("tactic"), f"{slug}: no tactic")

    def test_evidence_counts_match_examples(self):
        for slug, data in self.entries.items():
            self.assertEqual(data["repos"] >= len(data.get("examples") or []), True, slug)
            self.assertLessEqual(len(data.get("examples") or []), 5, slug)


if __name__ == "__main__":
    unittest.main()
