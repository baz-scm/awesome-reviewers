"""Tests for the published CLI, cli/awesome-reviewers.py.

Run from the repository root:

    python -m unittest discover -s tests -t .

Nothing here touches the network: the URL building, the selection and the retry
arithmetic are pure, and the one test that exercises `fetch` stubs urlopen.
"""

from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import re
import sys
import unittest
import urllib.error
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import build_data  # noqa: E402

CLI_PATH = ROOT / build_data.CLI_PATH.lstrip("/")


def load_cli():
    spec = importlib.util.spec_from_file_location("awesome_reviewers_cli", CLI_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


cli = load_cli()


ENTRIES = [
    {
        "slug": "kv-cache-reuse",
        "title": "Reuse the KV cache across requests",
        "description": "Avoid recomputing prefixes.",
        "repository": "vllm-project/vllm",
        "domain": "llm-infra",
        "topic": "Performance",
        "language": "Python",
        "updated": "2026-08-10",
        "comments": 7,
    },
    {
        "slug": "terraform-idempotent-applies",
        "title": "Keep applies idempotent",
        "description": "A second apply must be a no-op.",
        "repository": "hashicorp/terraform",
        "domain": "cloud-infra",
        "topic": "Configuration",
        "language": "Go",
        "updated": "2026-08-20",
        "comments": 3,
    },
]


class Urls(unittest.TestCase):
    """The CLI must call the endpoints the site actually publishes."""

    def test_matches_the_published_paths(self):
        expected = {
            ("version", ""): f"{build_data.API_BASE}/version.json",
            ("index", ""): f"{build_data.API_BASE}/index.json",
            ("domains", ""): f"{build_data.API_BASE}/domains.json",
            ("facets", ""): f"{build_data.API_BASE}/facets.json",
            ("sources", ""): f"{build_data.API_BASE}/sources.json",
            ("instruction", "a-slug"): f"{build_data.API_BASE}/instructions/a-slug.json",
            ("markdown", "a-slug"): "/raw/a-slug.md",
            ("bundle", "llm-infra"): "/raw/bundles/llm-infra.md",
        }
        for (kind, key), path in expected.items():
            with self.subTest(kind=kind):
                self.assertEqual(
                    cli.url_for(build_data.SITE_URL, kind, key),
                    f"{build_data.SITE_URL}{path}",
                )

    def test_defaults_to_the_production_site_and_tolerates_a_trailing_slash(self):
        self.assertEqual(cli.DEFAULT_SITE, build_data.SITE_URL)
        self.assertEqual(
            cli.url_for("https://example.test/", "version"),
            "https://example.test/v1/version.json",
        )

    def test_refuses_an_endpoint_it_does_not_know(self):
        with self.assertRaises(KeyError):
            cli.url_for(build_data.SITE_URL, "invented")

    def test_identifies_itself_and_points_at_the_docs(self):
        self.assertIn("awesome-reviewers-cli/", cli.USER_AGENT)
        self.assertIn(build_data.DEVELOPERS_URL, cli.USER_AGENT)

    def test_needs_nothing_but_the_standard_library(self):
        source = CLI_PATH.read_text(encoding="utf-8")
        imported = set(re.findall(r"^(?:from|import)\s+([a-zA-Z0-9_.]+)", source, re.MULTILINE))
        roots = {name.split(".")[0] for name in imported}
        self.assertTrue(roots.issubset(set(sys.stdlib_module_names)), roots)


class Selection(unittest.TestCase):
    def test_matches_every_term_across_the_useful_fields(self):
        self.assertEqual(
            [e["slug"] for e in cli.select(ENTRIES, "kv cache")], ["kv-cache-reuse"]
        )
        self.assertEqual(
            [e["slug"] for e in cli.select(ENTRIES, "terraform")],
            ["terraform-idempotent-applies"],
        )
        self.assertEqual(cli.select(ENTRIES, "kv terraform"), [])

    def test_filters_by_domain_topic_and_language(self):
        self.assertEqual(len(cli.select(ENTRIES, domain="llm-infra")), 1)
        self.assertEqual(len(cli.select(ENTRIES, topic="configuration")), 1)
        self.assertEqual(len(cli.select(ENTRIES, language="go")), 1)
        self.assertEqual(cli.select(ENTRIES, domain="security"), [])

    def test_sorts_newest_first_and_honours_the_limit(self):
        self.assertEqual(
            [e["slug"] for e in cli.select(ENTRIES)],
            ["terraform-idempotent-applies", "kv-cache-reuse"],
        )
        self.assertEqual(len(cli.select(ENTRIES, limit=1)), 1)


class Sync(unittest.TestCase):
    def test_fetches_only_what_changed(self):
        manifest = {"kv-cache-reuse": "2026-08-10"}
        stale = cli.sync_plan(ENTRIES, manifest)
        self.assertEqual([e["slug"] for e in stale], ["terraform-idempotent-applies"])

    def test_refetches_when_the_date_moved(self):
        manifest = {"kv-cache-reuse": "2026-01-01", "terraform-idempotent-applies": "2026-08-20"}
        stale = cli.sync_plan(ENTRIES, manifest)
        self.assertEqual([e["slug"] for e in stale], ["kv-cache-reuse"])

    def test_force_refetches_everything(self):
        manifest = {entry["slug"]: entry["updated"] for entry in ENTRIES}
        self.assertEqual(len(cli.sync_plan(ENTRIES, manifest, force=True)), len(ENTRIES))


class Pacing(unittest.TestCase):
    """The CLI waits as long as the interface tells it to, and no longer."""

    def test_prefers_retry_after(self):
        self.assertEqual(cli.retry_delay({"Retry-After": "12"}, 1), 12.0)

    def test_falls_back_to_the_ratelimit_window(self):
        self.assertEqual(cli.retry_delay({"RateLimit": '"default";r=0;t=41'}, 1), 41.0)

    def test_falls_back_to_a_backoff_when_neither_is_present(self):
        self.assertEqual(cli.retry_delay({}, 2), float(cli.FALLBACK_RETRY_SECONDS * 2))

    def test_ignores_a_malformed_value(self):
        self.assertEqual(cli.retry_delay({"Retry-After": "soon"}, 1), float(cli.FALLBACK_RETRY_SECONDS))

    def test_retries_a_429_then_succeeds(self):
        problem = json.dumps(
            {"code": "rate_limited", "detail": "The quota for this client is exhausted."}
        ).encode()
        attempts = []
        slept = []

        def urlopen(request, timeout=None):
            attempts.append(request.full_url)
            if len(attempts) == 1:
                raise urllib.error.HTTPError(
                    request.full_url, 429, "Too Many Requests", {"Retry-After": "3"}, io.BytesIO(problem)
                )
            return io.BytesIO(b'{"ok":true}')

        original = cli.urllib.request.urlopen
        cli.urllib.request.urlopen = urlopen
        try:
            body = cli.fetch("https://example.test/v1/version.json", sleep=slept.append)
        finally:
            cli.urllib.request.urlopen = original

        self.assertEqual(json.loads(body), {"ok": True})
        self.assertEqual(len(attempts), 2)
        self.assertEqual(slept, [3.0])

    def test_reports_the_resolution_from_a_problem_body(self):
        problem = json.dumps(
            {"detail": "Nothing is published at this path.", "resolution": "Look it up in the index."}
        ).encode()

        def urlopen(request, timeout=None):
            raise urllib.error.HTTPError(
                request.full_url, 404, "Not Found", {}, io.BytesIO(problem)
            )

        original = cli.urllib.request.urlopen
        cli.urllib.request.urlopen = urlopen
        try:
            with self.assertRaises(cli.ApiError) as raised:
                cli.fetch("https://example.test/raw/nope.md")
        finally:
            cli.urllib.request.urlopen = original

        self.assertEqual(raised.exception.status, 404)
        self.assertIn("Nothing is published", str(raised.exception))
        self.assertIn("Look it up in the index.", str(raised.exception))


class Parser(unittest.TestCase):
    def test_every_documented_command_parses(self):
        parser = cli.build_parser()
        for argv in (
            ["version"],
            ["domains", "--json"],
            ["search", "kv cache", "--limit", "5"],
            ["search", "--domain", "security"],
            ["get", "a-slug"],
            ["get", "a-slug", "--json", "-o", "out.json"],
            ["bundle", "llm-infra", "-o", "rubric.md"],
            ["sync", "./corpus", "--domain", "security", "--force"],
        ):
            with self.subTest(argv=argv):
                args = parser.parse_args(argv)
                self.assertTrue(callable(args.func))
                self.assertEqual(args.site, build_data.SITE_URL)

    def test_the_site_can_be_pointed_at_a_local_build(self):
        args = cli.build_parser().parse_args(["--site", "http://localhost:4000", "version"])
        self.assertEqual(args.site, "http://localhost:4000")

    def test_a_command_is_required(self):
        with self.assertRaises(SystemExit), contextlib.redirect_stderr(io.StringIO()):
            cli.build_parser().parse_args([])

    def test_the_documented_commands_are_the_ones_the_portal_lists(self):
        portal = (ROOT / "developers.md").read_text(encoding="utf-8")
        for command in ("domains", "search", "get", "bundle", "sync"):
            with self.subTest(command=command):
                self.assertIn(f"awesome-reviewers.py {command}", portal)


if __name__ == "__main__":
    unittest.main()
