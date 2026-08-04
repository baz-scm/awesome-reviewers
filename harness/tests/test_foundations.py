"""Digests, credential scrubbing, and path confinement.

Everything above these is a digest of something, a redaction of something, or a path
that must not escape, so these are tested for their invariants rather than their
happy paths.
"""

from __future__ import annotations

import io
import tarfile
import tempfile
import unittest
from pathlib import Path

from awesome_harness import digest as D
from awesome_harness import scrub
from awesome_harness.errors import IntegrityError
from awesome_harness.paths import PathEscape, is_within, resolve_within, safe_extract


class TestCanonicalJson(unittest.TestCase):
    def test_key_order_does_not_change_the_digest(self) -> None:
        self.assertEqual(
            D.digest_json({"a": 1, "b": {"c": 2, "d": 3}}),
            D.digest_json({"b": {"d": 3, "c": 2}, "a": 1}),
        )

    def test_no_incidental_whitespace(self) -> None:
        self.assertEqual(D.canonical_json({"a": [1, 2]}), b'{"a":[1,2]}')

    def test_nan_is_refused_rather_than_emitted(self) -> None:
        # json would happily write NaN, which is not JSON, so a digest over it would
        # commit to bytes no other language can parse.
        with self.assertRaises(ValueError):
            D.canonical_json({"x": float("nan")})

    def test_digest_set_is_order_independent(self) -> None:
        a = D.digest_bytes(b"a")
        b = D.digest_bytes(b"b")
        self.assertEqual(D.digest_set([a, b]), D.digest_set([b, a, b]))


class TestFileDigests(unittest.TestCase):
    def test_absent_and_empty_are_different(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "empty.txt").write_bytes(b"")
            tree = D.digest_tree(root, ["empty.txt", "missing.txt"])
            self.assertEqual(tree["missing.txt"], D.ABSENT)
            self.assertTrue(D.is_digest(tree["empty.txt"]))
            self.assertNotEqual(tree["empty.txt"], tree["missing.txt"])

    def test_streaming_digest_matches_bytes_digest(self) -> None:
        payload = b"x" * (D.CHUNK_BYTES + 17)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "big.bin"
            path.write_bytes(payload)
            self.assertEqual(D.digest_file(path), D.digest_bytes(payload))

    def test_require_digest_rejects_malformed(self) -> None:
        for bad in ("sha256:xyz", "deadbeef", "", None, "sha1:" + "a" * 40):
            with self.assertRaises(IntegrityError):
                D.require_digest(bad)

    def test_zero_sentinel_is_accepted_as_a_digest(self) -> None:
        # The genesis record's `prev` must verify through the same code path as any
        # other record's.
        self.assertTrue(D.is_digest(D.ZERO))


class TestScrub(unittest.TestCase):
    def test_provider_tokens_are_redacted(self) -> None:
        samples = {
            "aws-access-key-id": "AKIAIOSFODNN7EXAMPLE",
            "github-token": "ghp_" + "a" * 36,
            "slack-token": "xoxb-1234567890-abcdefghij",
            "google-api-key": "AIza" + "b" * 35,
            "anthropic-api-key": "sk-ant-" + "c" * 40,
            "stripe-key": "sk_live_" + "d" * 24,
            "npm-token": "npm_" + "e" * 36,
            "jwt": "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.dBjftJeZ4CVPmB92K27uhbUJU1p",
        }
        for label, secret in samples.items():
            cleaned, hits = scrub.scrub(f"value = {secret}")
            self.assertNotIn(secret, cleaned, label)
            self.assertIn(label, hits, label)

    def test_placeholders_survive(self) -> None:
        for text in (
            "token = ${CI_TOKEN}",
            "password: <your-password>",
            "api_key = $API_KEY",
            "secret: changeme",
            "password = ***",
        ):
            cleaned, hits = scrub.scrub(text)
            self.assertEqual(cleaned, text, text)
            self.assertEqual(hits, [], text)

    def test_scrubbing_is_idempotent(self) -> None:
        once = scrub.scrub_text("Authorization: Bearer abcdef1234567890")
        self.assertEqual(scrub.scrub_text(once), once)

    def test_url_credentials_lose_only_the_password(self) -> None:
        cleaned = scrub.scrub_text("git remote add origin https://user:hunter2secret@example.com/x.git")
        self.assertNotIn("hunter2secret", cleaned)
        self.assertIn("user", cleaned)
        self.assertIn("example.com", cleaned)

    def test_env_is_redacted_by_name_not_only_by_shape(self) -> None:
        out = scrub.scrub_env({"DEPLOY_TOKEN": "plainlooking", "PATH": "/usr/bin"})
        self.assertNotIn("plainlooking", out["DEPLOY_TOKEN"])
        self.assertEqual(out["PATH"], "/usr/bin")

    def test_argv_is_scrubbed(self) -> None:
        argv = scrub.scrub_argv(["curl", "-H", "Authorization: Bearer abcdef1234567890"])
        self.assertNotIn("abcdef1234567890", " ".join(argv))

    def test_high_confidence_tier_ignores_generic_assignments(self) -> None:
        # The blocking tier must not fire on `password = value`, or the gate would
        # block on every configuration example in a repository.
        _, hits = scrub.scrub("password = correct-horse-battery", scrub.HIGH_CONFIDENCE)
        self.assertEqual(hits, [])


class TestPathConfinement(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.base = Path(self._tmp.name).resolve() / "run"
        self.base.mkdir(parents=True)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_sibling_prefix_is_not_inside(self) -> None:
        # The bypass a `startswith` check misses: /run is a string prefix of /runner.
        sibling = self.base.parent / "runner"
        sibling.mkdir()
        self.assertFalse(is_within(self.base, sibling))
        self.assertTrue(str(sibling).startswith(str(self.base)))

    def test_traversal_is_rejected(self) -> None:
        for candidate in ("../escape", "a/../../escape", "./../x"):
            with self.assertRaises(PathEscape, msg=candidate):
                resolve_within(self.base, candidate)

    def test_absolute_paths_are_rejected_not_rerooted(self) -> None:
        with self.assertRaises(PathEscape):
            resolve_within(self.base, "/etc/passwd")

    def test_normal_relative_path_resolves(self) -> None:
        self.assertEqual(resolve_within(self.base, "a/b.txt"), self.base / "a" / "b.txt")

    def _tar_with(self, name: str, *, linkname: str = "", kind: bytes = tarfile.REGTYPE) -> Path:
        path = self.base / "evil.tar"
        with tarfile.open(path, "w") as tar:
            info = tarfile.TarInfo(name=name)
            info.type = kind
            if linkname:
                info.linkname = linkname
                info.size = 0
                tar.addfile(info)
            else:
                data = b"payload"
                info.size = len(data)
                tar.addfile(info, io.BytesIO(data))
        return path

    def test_extraction_rejects_traversal(self) -> None:
        archive = self._tar_with("../../etc/passwd")
        with tarfile.open(archive) as tar, self.assertRaises(PathEscape):
            safe_extract(tar, self.base / "out")

    def test_extraction_rejects_absolute_members(self) -> None:
        archive = self._tar_with("/etc/passwd")
        with tarfile.open(archive) as tar, self.assertRaises(PathEscape):
            safe_extract(tar, self.base / "out")

    def test_extraction_rejects_symlinks_by_default(self) -> None:
        archive = self._tar_with("link", linkname="/etc/passwd", kind=tarfile.SYMTYPE)
        with tarfile.open(archive) as tar, self.assertRaises(PathEscape):
            safe_extract(tar, self.base / "out")

    def test_extraction_accepts_ordinary_members(self) -> None:
        archive = self._tar_with("nested/ok.txt")
        with tarfile.open(archive) as tar:
            names = safe_extract(tar, self.base / "out")
        self.assertEqual(names, ["nested/ok.txt"])
        self.assertTrue((self.base / "out" / "nested" / "ok.txt").is_file())


if __name__ == "__main__":
    unittest.main()
