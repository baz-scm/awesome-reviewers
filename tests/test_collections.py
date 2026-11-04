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


class TechniqueTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.entries = {p.stem: load(p) for p in sorted((ROOT / "_verification").glob("*.md"))}

    def test_ids_are_unique_and_well_formed(self):
        ids = [data["id"] for data in self.entries.values()]
        self.assertEqual(len(ids), len(set(ids)), "technique ids must be unique")
        for data in self.entries.values():
            self.assertRegex(data["id"], TECHNIQUE_ID)

    def test_subtechniques_extend_their_parent_id(self):
        for slug, data in self.entries.items():
            for sub in data.get("subtechniques") or []:
                self.assertRegex(sub["id"], SUBTECHNIQUE_ID, slug)
                self.assertTrue(sub["id"].startswith(data["id"] + "."), f"{slug}: {sub['id']} under {data['id']}")

    def test_every_technique_has_craft_and_signals(self):
        for slug, data in self.entries.items():
            self.assertTrue(data.get("craft"), f"{slug}: no craft steps")
            self.assertTrue(data.get("reverse"), f"{slug}: no signals")
            self.assertTrue(data.get("tactic"), f"{slug}: no tactic")


if __name__ == "__main__":
    unittest.main()
