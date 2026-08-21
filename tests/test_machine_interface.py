"""Tests for the machine interface: OpenAPI, error format, llms.txt, 404, discovery links.

Run from the repository root:

    python -m unittest discover -s tests -t .

The derived artifacts are built on demand if they are missing, so this needs no
setup beyond a checkout.
"""

from __future__ import annotations

import json
import os
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import build_data  # noqa: E402


def setUpModule() -> None:
    os.chdir(ROOT)
    if not build_data.OPENAPI_PATH.exists():
        build_data.main()


ENTRIES = [
    {
        "slug": "example-instruction",
        "title": "Example instruction",
        "description": "An example.",
        "repository": "example/repo",
        "domain": "ai-agents",
        "topic": "AI",
        "language": "Python",
        "updated": "2026-08-12",
        "comments": 3,
        "stars": 10,
    },
    {
        "slug": "other-instruction",
        "title": "Other instruction",
        "description": "Another example.",
        "repository": "example/other",
        "domain": "devtools",
        "topic": "Testing",
        "language": "Go",
        "updated": "2026-08-01",
        "comments": 1,
        "stars": 5,
    },
]

DOMAINS = [
    {
        "slug": "ai-agents",
        "title": "AI Agents & Assistants",
        "blurb": "Agent loops and tool calling.",
        "count": 1,
        "repositories": 1,
        "updated": "2026-08-12",
        "topics": ["AI"],
        "languages": ["Python"],
    },
    {
        "slug": "devtools",
        "title": "Developer Tooling",
        "blurb": "Editors and build systems.",
        "count": 1,
        "repositories": 1,
        "updated": "2026-08-01",
        "topics": ["Testing"],
        "languages": ["Go"],
    },
]

VERSION = "2026-08-12"


class ProblemTypes(unittest.TestCase):
    """RFC 9457 problem details, with the `code` and `resolution` extensions."""

    def test_every_problem_is_complete(self):
        for problem in build_data.build_problems():
            with self.subTest(code=problem["code"]):
                for member in ("type", "title", "status", "detail", "code", "resolution"):
                    self.assertTrue(problem[member], f"{member} is empty")
                self.assertIsInstance(problem["status"], int)

    def test_codes_are_unique(self):
        codes = [problem["code"] for problem in build_data.build_problems()]
        self.assertCountEqual(codes, set(codes))

    def test_type_uri_resolves_to_its_documentation_anchor(self):
        # The API page renders one <h3 id="error-<code>"> per problem type, so a
        # client that dereferences `type` lands on the description of that error.
        api_page = (ROOT / "api.html").read_text(encoding="utf-8")
        self.assertIn("""id="error-{{ error.code | replace: '_', '-' }}\"""", api_page)
        for problem in build_data.build_problems():
            with self.subTest(code=problem["code"]):
                anchor = problem["code"].replace("_", "-")
                self.assertEqual(
                    problem["type"],
                    f"{build_data.SITE_URL}/api/#error-{anchor}",
                )

    def test_404_and_406_are_described(self):
        statuses = {problem["status"] for problem in build_data.build_problems()}
        self.assertEqual(statuses, {404, 406})


class OpenAPIDocument(unittest.TestCase):
    def setUp(self):
        self.doc = build_data.build_openapi(ENTRIES, DOMAINS, VERSION)

    def test_is_openapi_31_and_named_after_the_product(self):
        self.assertEqual(self.doc["openapi"], "3.1.0")
        self.assertEqual(self.doc["info"]["title"], "Awesome Reviewers API")
        self.assertEqual(self.doc["info"]["version"], VERSION)
        self.assertEqual(self.doc["servers"][0]["url"], build_data.SITE_URL)

    def test_documents_every_published_resource(self):
        # DEV_RESOURCES is what the site advertises; anything advertised and not
        # described here would be a path an agent can find but not understand.
        described = set(self.doc["paths"])
        templated = {
            "/raw/<slug>.md": "/raw/{slug}.md",
            "/raw/bundles/<domain>.md": "/raw/bundles/{domain}.md",
            "/<slug>.json": "/{slug}.json",
        }
        self.assertIn("/raw/site.md", described)
        for resource in build_data.DEV_RESOURCES:
            path = resource["path"]
            if path == "/api/":  # documentation, not an endpoint
                continue
            with self.subTest(path=path):
                self.assertIn(templated.get(path, path), described)

    def test_every_operation_is_a_documented_get(self):
        seen_ids = set()
        for path, item in self.doc["paths"].items():
            with self.subTest(path=path):
                self.assertEqual(list(item), ["get"], "endpoints are GET only")
                operation = item["get"]
                self.assertTrue(operation["summary"])
                self.assertNotIn(operation["operationId"], seen_ids)
                seen_ids.add(operation["operationId"])
                self.assertIn("200", operation["responses"])

    def test_error_responses_offer_problem_json(self):
        operation = self.doc["paths"]["/raw/{slug}.md"]["get"]
        for status in ("404", "406"):
            content = operation["responses"][status]["content"]
            self.assertIn("application/problem+json", content)
            example = content["application/problem+json"]["example"]
            self.assertEqual(example["status"], int(status))
            self.assertTrue(example["resolution"])
            # The HTML variant is what static hosting actually serves; it is
            # documented so a client is not surprised by it.
            self.assertIn("text/html", content)

    def test_problem_schema_follows_rfc_9457(self):
        problem = self.doc["components"]["schemas"]["Problem"]
        self.assertEqual(problem["required"], ["type", "title", "status"])
        for member in ("type", "title", "status", "detail", "instance", "code", "resolution"):
            self.assertIn(member, problem["properties"])
        self.assertEqual(
            problem["properties"]["code"]["enum"],
            [p["code"] for p in build_data.build_problems()],
        )

    def test_domain_enum_comes_from_the_corpus(self):
        parameter = self.doc["paths"]["/raw/bundles/{domain}.md"]["get"]["parameters"][0]
        self.assertEqual(parameter["schema"]["enum"], [d["slug"] for d in DOMAINS])

    def test_every_ref_resolves(self):
        components = self.doc["components"]
        refs = []

        def walk(node):
            if isinstance(node, dict):
                if "$ref" in node:
                    refs.append(node["$ref"])
                for value in node.values():
                    walk(value)
            elif isinstance(node, list):
                for value in node:
                    walk(value)

        walk(self.doc)
        self.assertTrue(refs)
        for ref in refs:
            with self.subTest(ref=ref):
                prefix, _, name = ref.rpartition("/")
                section = prefix.rsplit("/", 1)[-1]
                self.assertIn(name, components[section])

    def test_validates_against_the_openapi_31_schema(self):
        # Optional: the deploy pipeline must not depend on a package index, so
        # this runs wherever the validator happens to be installed.
        #   pip install openapi-spec-validator
        try:
            from openapi_spec_validator import validate
        except ImportError:  # pragma: no cover - depends on the environment
            self.skipTest("openapi-spec-validator is not installed")
        validate(json.loads(build_data.OPENAPI_PATH.read_text(encoding="utf-8")))

    def test_published_document_matches_the_builder(self):
        published = json.loads(build_data.OPENAPI_PATH.read_text(encoding="utf-8"))
        self.assertEqual(published["openapi"], "3.1.0")
        self.assertEqual(published["info"]["title"], "Awesome Reviewers API")
        self.assertEqual(set(published["paths"]), set(self.doc["paths"]))
        index_entries = published["paths"]["/raw/index.json"]["get"]["responses"]["200"]
        self.assertIn("application/json", index_entries["content"])


class SiteOverview(unittest.TestCase):
    """The short markdown representation of the homepage."""

    def setUp(self):
        self.text = build_data.build_site_overview(ENTRIES, DOMAINS)

    def test_names_the_product_and_counts_the_corpus(self):
        self.assertTrue(self.text.startswith("# Awesome Reviewers\n"))
        self.assertIn(f"{len(ENTRIES)} instructions", self.text)

    def test_lists_every_developer_resource_and_domain(self):
        for resource in build_data.DEV_RESOURCES:
            self.assertIn(f"{build_data.SITE_URL}{resource['path']}", self.text)
        for domain in DOMAINS:
            self.assertIn(f"{build_data.SITE_URL}/raw/bundles/{domain['slug']}.md", self.text)

    def test_is_short_enough_to_be_worth_serving_as_the_homepage(self):
        # llms.txt lists every instruction; this is the one-screen version.
        self.assertLess(len(self.text), 8000)

    def test_published_file_agrees(self):
        published = (build_data.RAW_DIR / "site.md").read_text(encoding="utf-8")
        self.assertTrue(published.startswith("# Awesome Reviewers\n"))
        self.assertIn(f"{build_data.SITE_URL}/openapi.json", published)
        self.assertLess(len(published), 8000)


class LlmsTxt(unittest.TestCase):
    def setUp(self):
        self.text = "\n".join(build_data.build_llms(ENTRIES, DOMAINS))

    def test_names_the_api_and_lists_every_resource(self):
        self.assertIn("## Awesome Reviewers API — developer resources", self.text)
        for resource in build_data.DEV_RESOURCES:
            with self.subTest(resource=resource["name"]):
                self.assertIn(resource["name"], self.text)
                self.assertIn(f"{build_data.SITE_URL}{resource['path']}", self.text)

    def test_documents_the_error_format(self):
        self.assertIn("RFC 9457", self.text)
        for problem in build_data.build_problems():
            self.assertIn(problem["code"], self.text)
            self.assertIn(problem["type"], self.text)

    def test_documents_the_markdown_variants(self):
        self.assertIn("/raw/<slug>.md", self.text)
        self.assertIn("/raw/bundles/<domain>.md", self.text)
        self.assertIn('rel="alternate"', self.text)

    def test_published_file_agrees(self):
        published = build_data.LLMS_PATH.read_text(encoding="utf-8")
        self.assertIn("## Awesome Reviewers API — developer resources", published)
        self.assertIn(f"{build_data.SITE_URL}/openapi.json", published)


class NotFoundPage(unittest.TestCase):
    """The 404 body has to let an agent recover without a second guess."""

    def setUp(self):
        self.source = (ROOT / "404.html").read_text(encoding="utf-8")

    def test_is_published_at_the_path_github_pages_serves(self):
        self.assertIn("permalink: /404.html", self.source)

    def test_points_at_every_index(self):
        for target in ("/raw/index.json", "/llms.txt", "/openapi.json", "/sitemap.xml", "/api/"):
            with self.subTest(target=target):
                self.assertIn(target, self.source)

    def test_carries_a_markdown_recovery_body(self):
        self.assertIn("# 404 Not Found", self.source)
        self.assertIn("## Recover", self.source)

    def test_carries_the_problem_details_for_machines(self):
        self.assertIn('<script type="application/problem+json" id="problem">', self.source)
        self.assertIn('"status": 404', self.source)
        self.assertIn('"code": "not_found"', self.source)


class DiscoveryLinks(unittest.TestCase):
    def setUp(self):
        self.base = (ROOT / "_layouts" / "base.html").read_text(encoding="utf-8")

    def test_every_page_advertises_the_openapi_description(self):
        self.assertIn('rel="service-desc"', self.base)
        self.assertIn("/openapi.json", self.base)
        self.assertIn('rel="service-doc"', self.base)

    def test_pages_with_a_markdown_twin_advertise_it(self):
        self.assertIn('rel="alternate" type="text/markdown"', self.base)
        self.assertIn("'/raw/' | append: page.slug | append: '.md'", self.base)
        self.assertIn("'/raw/bundles/' | append: page.domain | append: '.md'", self.base)

    def test_robots_lists_the_developer_resources(self):
        robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
        self.assertIn("Sitemap: https://awesomereviewers.com/sitemap.xml", robots)
        for path in ("/openapi.json", "/api/", "/llms.txt", "/raw/index.json"):
            with self.subTest(path=path):
                self.assertIn(path, robots)

    def test_api_page_is_discoverable_by_name(self):
        api_page = (ROOT / "api.html").read_text(encoding="utf-8")
        self.assertIn("<h1>Awesome Reviewers API</h1>", api_page)
        self.assertIn('"@type": "WebAPI"', api_page)
        self.assertIn('"name": "Awesome Reviewers API"', api_page)


class BuildHygiene(unittest.TestCase):
    def test_derived_artifacts_are_not_committed(self):
        ignored = (ROOT / ".gitignore").read_text(encoding="utf-8").split()
        for path in ("openapi.json", "_data/api.json", "llms.txt"):
            with self.subTest(path=path):
                self.assertIn(path, ignored)

    def test_the_edge_worker_and_tests_are_not_published(self):
        config = (ROOT / "_config.yml").read_text(encoding="utf-8")
        self.assertIn("- edge/", config)
        self.assertIn("- tests/", config)

    def test_raw_markdown_carries_no_front_matter(self):
        # Front matter would make Jekyll render these as pages instead of
        # serving them verbatim.
        sample = sorted(build_data.RAW_DIR.glob("*.md"))[:20]
        self.assertTrue(sample)
        for path in sample:
            with self.subTest(path=path.name):
                self.assertFalse(path.read_text(encoding="utf-8").startswith("---"))


if __name__ == "__main__":
    unittest.main()
