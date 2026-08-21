"""Tests for the machine interface: OpenAPI, the versioned JSON surface, the error
format, llms.txt, agents.md, the 404 body, the trust pages and the discovery links.

Run from the repository root:

    python -m unittest discover -s tests -t .

The derived artifacts are built on demand if they are missing, so this needs no
setup beyond a checkout.
"""

from __future__ import annotations

import json
import os
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import build_data  # noqa: E402


def setUpModule() -> None:
    os.chdir(ROOT)
    if not build_data.OPENAPI_PATH.exists() or not (build_data.V1_DIR / "version.json").exists():
        build_data.main()


def published(path: Path | str) -> object:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def liquid_free(text: str) -> str:
    """A Liquid template with every expression replaced by a placeholder.

    The JSON-LD blocks are Liquid templates, so they cannot be parsed as JSON as
    they stand. Every expression in them sits inside a JSON string, which makes
    substitution enough to assert on the structure.
    """
    return re.sub(r"\{\{.*?\}\}", "x", text, flags=re.DOTALL)


def json_ld(source: str) -> list:
    blocks = re.findall(
        r'<script type="application/ld\+json">(.*?)</script>', source, flags=re.DOTALL
    )
    return [json.loads(liquid_free(block)) for block in blocks]


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
        "first_seen": "2026-01-04",
        "comments": 3,
        "discussions": 2,
        "stars": 10,
        "authors": ["reviewer-one", "reviewer-two"],
        "body": "Do the thing.",
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
        "first_seen": "2026-02-02",
        "comments": 1,
        "discussions": 1,
        "stars": 5,
        "authors": ["reviewer-one"],
        "body": "Do the other thing.",
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
GENERATED = "2026-08-12T00:00:00Z"


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

    def test_404_406_and_429_are_described(self):
        statuses = {problem["status"] for problem in build_data.build_problems()}
        self.assertEqual(statuses, {404, 406, 429})

    def test_rate_limit_problem_says_how_long_to_wait(self):
        problem = next(
            p for p in build_data.build_problems() if p["code"] == "rate_limited"
        )
        self.assertIn("Retry-After", problem["resolution"])
        self.assertIn(str(build_data.RATE_LIMIT_QUOTA), problem["resolution"])

    def test_every_problem_is_published_as_a_document(self):
        catalog = published(build_data.V1_DIR / "errors" / "index.json")
        self.assertEqual(catalog["count"], len(build_data.PROBLEM_TYPES))
        for problem in build_data.build_problems():
            with self.subTest(code=problem["code"]):
                document = published(
                    ROOT / build_data.problem_document_path(problem["code"]).lstrip("/")
                )
                self.assertEqual(document, problem)


class OpenAPIDocument(unittest.TestCase):
    def setUp(self):
        self.doc = build_data.build_openapi(ENTRIES, DOMAINS, VERSION)
        self.operations = {
            path: item["get"] for path, item in self.doc["paths"].items()
        }

    def test_is_openapi_31_and_named_after_the_product(self):
        self.assertEqual(self.doc["openapi"], "3.1.0")
        self.assertEqual(self.doc["info"]["title"], "Awesome Reviewers API")
        self.assertEqual(self.doc["info"]["version"], VERSION)
        self.assertEqual(self.doc["servers"][0]["url"], build_data.SITE_URL)

    def test_declares_the_interface_version_and_its_policy(self):
        # `info.version` is the corpus date; the interface version is what a
        # client integrates against, and it has to be legible on its own.
        self.assertEqual(self.doc["x-api-version"], build_data.API_VERSION)
        versioning = self.doc["x-versioning"]
        self.assertEqual(versioning["scheme"], "url-path")
        self.assertEqual(versioning["base_path"], build_data.API_BASE)
        self.assertEqual(versioning["stability"], "stable")
        self.assertTrue(versioning["compatible_changes"])
        self.assertTrue(versioning["breaking_changes"])
        self.assertGreaterEqual(versioning["sunset_notice_days"], 90)
        self.assertIn("Deprecation", versioning["deprecation"])
        self.assertIn("Sunset", versioning["deprecation"])
        self.assertIn("/v1/", self.doc["info"]["description"])

    def test_every_versioned_path_sits_under_the_version_prefix(self):
        versioned = [p for p in self.doc["paths"] if p.startswith(build_data.API_BASE)]
        self.assertGreaterEqual(len(versioned), 8)
        for path in versioned:
            with self.subTest(path=path):
                self.assertTrue(path.startswith(f"{build_data.API_BASE}/"))

    def test_declares_the_rate_limit_policy_and_its_headers(self):
        limit = self.doc["x-rate-limit"]
        self.assertEqual(
            limit["policy"],
            f'"{build_data.RATE_LIMIT_NAME}";q={build_data.RATE_LIMIT_QUOTA};'
            f"w={build_data.RATE_LIMIT_WINDOW}",
        )
        self.assertEqual(limit["quota"], build_data.RATE_LIMIT_QUOTA)
        self.assertEqual(limit["window_seconds"], build_data.RATE_LIMIT_WINDOW)
        # Honesty about who applies it matters as much as the number.
        self.assertEqual(limit["origin"], "none")
        self.assertEqual(limit["enforced_by"], "edge")
        for header in ("RateLimitPolicy", "RateLimit", "RetryAfter", "Deprecation", "Sunset"):
            self.assertIn(header, self.doc["components"]["headers"])

    def test_documents_every_published_resource(self):
        # DEV_RESOURCES is what the site advertises; anything advertised and not
        # described here would be a path an agent can find but not understand.
        described = set(self.doc["paths"])
        templated = {
            "/raw/<slug>.md": "/raw/{slug}.md",
            "/raw/bundles/<domain>.md": "/raw/bundles/{domain}.md",
            "/<slug>.json": "/{slug}.json",
            f"{build_data.API_BASE}/instructions/<slug>.json": (
                f"{build_data.API_BASE}/instructions/{{slug}}.json"
            ),
            f"{build_data.API_BASE}/errors/<code>.json": (
                f"{build_data.API_BASE}/errors/{{code}}.json"
            ),
        }
        self.assertIn("/raw/site.md", described)
        for resource in build_data.DEV_RESOURCES:
            if resource.get("docs"):  # a page to read, not an endpoint to call
                continue
            path = resource["path"]
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

    def test_every_operation_is_callable_from_a_function_definition(self):
        # An LLM function-calling layer needs a unique name, a description of
        # what the call does, and a typed response for every operation.
        for path, operation in self.operations.items():
            with self.subTest(path=path):
                self.assertRegex(operation["operationId"], r"^[a-zA-Z][a-zA-Z0-9_]*$")
                self.assertTrue(operation.get("description"), "no description")
                self.assertTrue(operation["tags"])
                content = operation["responses"]["200"]["content"]
                self.assertTrue(content, "no response content")
                for media_type, media in content.items():
                    self.assertIn("schema", media, media_type)
                for parameter in operation.get("parameters", []):
                    if "$ref" in parameter:
                        continue
                    self.assertIn("schema", parameter)
                    self.assertTrue(parameter.get("description"))

    def test_most_operations_return_a_typed_json_object(self):
        # The rest are markdown, plain text, XML or a Python file: formats that
        # cannot be JSON without being something other than what they are.
        typed = [
            path
            for path, operation in self.operations.items()
            if "$ref" in str(operation["responses"]["200"]["content"].get("application/json", {}))
        ]
        self.assertGreaterEqual(len(typed), 11)
        self.assertGreaterEqual(len(typed) / len(self.operations), 0.5)
        for path in (
            "/raw/index.json",
            f"{build_data.API_BASE}/index.json",
            f"{build_data.API_BASE}/version.json",
            f"{build_data.API_BASE}/instructions/{{slug}}.json",
            f"{build_data.API_BASE}/domains.json",
            f"{build_data.API_BASE}/facets.json",
            f"{build_data.API_BASE}/sources.json",
            f"{build_data.API_BASE}/errors/index.json",
            f"{build_data.API_BASE}/errors/{{code}}.json",
        ):
            with self.subTest(path=path):
                self.assertIn(path, typed)

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

    def test_every_operation_documents_the_quota_response(self):
        for path, operation in self.operations.items():
            with self.subTest(path=path):
                self.assertIn("429", operation["responses"], "429 is undocumented")
                headers = operation["responses"]["429"]["headers"]
                self.assertIn("Retry-After", headers)
                self.assertIn("RateLimit", headers)

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
        validate(published(build_data.OPENAPI_PATH))

    def test_published_document_matches_the_builder(self):
        document = published(build_data.OPENAPI_PATH)
        self.assertEqual(document["openapi"], "3.1.0")
        self.assertEqual(document["info"]["title"], "Awesome Reviewers API")
        self.assertEqual(set(document["paths"]), set(self.doc["paths"]))
        index_entries = document["paths"]["/raw/index.json"]["get"]["responses"]["200"]
        self.assertIn("application/json", index_entries["content"])

    def test_the_versioned_copy_is_the_same_document(self):
        self.assertEqual(
            published(build_data.OPENAPI_PATH),
            published(build_data.V1_DIR / "openapi.json"),
        )


class VersionedSurface(unittest.TestCase):
    """`/v1/**`: the shapes a client integrates against."""

    def setUp(self):
        self.version = build_data.build_version(ENTRIES, VERSION, GENERATED)

    def test_states_the_version_the_corpus_date_and_the_authentication(self):
        self.assertEqual(self.version["api_version"], build_data.API_VERSION)
        self.assertEqual(self.version["base_url"], build_data.API_BASE_URL)
        self.assertEqual(self.version["corpus_version"], VERSION)
        self.assertEqual(self.version["count"], len(ENTRIES))
        self.assertEqual(self.version["authentication"], "none")

    def test_publishes_the_versioning_policy_a_client_can_rely_on(self):
        policy = self.version["versioning"]
        self.assertEqual(policy["current"], build_data.API_VERSION)
        self.assertIn("/v2", policy["breaking_change_process"])
        self.assertEqual(policy["sunset_notice_days"], build_data.SUNSET_NOTICE_DAYS)
        self.assertEqual(self.version["deprecations"], [])

    def test_publishes_the_rate_limit_policy_in_the_header_syntax(self):
        limit = self.version["rate_limit"]
        self.assertEqual(limit["quota"], build_data.RATE_LIMIT_QUOTA)
        self.assertRegex(limit["policy"], r'^"[a-z]+";q=\d+;w=\d+$')
        self.assertIn("RateLimit-Policy", limit["headers"])
        self.assertIn("Retry-After", limit["headers"])
        self.assertEqual(limit["on_exceeded"]["status"], 429)

    def test_lists_every_resource_with_an_absolute_url(self):
        urls = {resource["url"] for resource in self.version["resources"]}
        for resource in build_data.DEV_RESOURCES:
            with self.subTest(path=resource["path"]):
                self.assertIn(f"{build_data.SITE_URL}{resource['path']}", urls)

    def test_published_file_agrees(self):
        document = published(build_data.V1_DIR / "version.json")
        self.assertEqual(document["api_version"], build_data.API_VERSION)
        self.assertEqual(document["versioning"]["base_path"], build_data.API_BASE)
        self.assertEqual(
            document["api_catalog"],
            f"{build_data.SITE_URL}/{build_data.API_CATALOG_PATH.as_posix()}",
        )

    def test_the_index_carries_a_json_url_for_every_entry(self):
        payload = build_data.build_index_payload(ENTRIES, DOMAINS, GENERATED)
        self.assertEqual(payload["api_version"], build_data.API_VERSION)
        for entry in payload["entries"]:
            with self.subTest(slug=entry["slug"]):
                self.assertEqual(
                    entry["json"],
                    f"{build_data.API_BASE_URL}/instructions/{entry['slug']}.json",
                )
                self.assertEqual(entry["raw"], f"{build_data.SITE_URL}/raw/{entry['slug']}.md")

    def test_an_instruction_document_carries_the_body_and_its_links(self):
        document = build_data.build_instruction(ENTRIES[0])
        self.assertEqual(document["body"], ENTRIES[0]["body"])
        self.assertEqual(document["media_type"], "text/markdown")
        self.assertEqual(document["reviewers"], ENTRIES[0]["authors"])
        self.assertEqual(
            document["links"]["markdown"],
            f"{build_data.SITE_URL}/raw/{ENTRIES[0]['slug']}.md",
        )
        self.assertEqual(
            document["links"]["page"],
            f"{build_data.SITE_URL}/reviewers/{ENTRIES[0]['slug']}/",
        )

    def test_published_instruction_documents_match_their_markdown(self):
        index = published(build_data.V1_DIR / "index.json")
        for entry in index["entries"][:25]:
            slug = entry["slug"]
            with self.subTest(slug=slug):
                document = published(build_data.V1_DIR / "instructions" / f"{slug}.json")
                markdown = (build_data.RAW_DIR / f"{slug}.md").read_text(encoding="utf-8")
                self.assertEqual(document["slug"], slug)
                self.assertEqual(document["title"], entry["title"])
                self.assertEqual(document["updated"], entry["updated"])
                self.assertTrue(document["body"])
                # The markdown endpoint is the same body behind a comment header.
                self.assertIn(document["body"].strip(), markdown)

    def test_domains_facets_and_sources_are_published_and_counted(self):
        domains = build_data.build_domains_payload(DOMAINS, GENERATED)
        self.assertEqual(domains["count"], len(DOMAINS))
        self.assertEqual(
            domains["domains"][0]["bundle"],
            f"{build_data.SITE_URL}/raw/bundles/{DOMAINS[0]['slug']}.md",
        )

        facets = build_data.build_facets(ENTRIES, DOMAINS)
        self.assertEqual(
            {facet["value"] for facet in facets["topics"]},
            {entry["topic"] for entry in ENTRIES},
        )
        self.assertEqual(sum(facet["count"] for facet in facets["languages"]), len(ENTRIES))

        sources = build_data.build_sources_payload(ENTRIES, GENERATED)
        self.assertEqual(sources["count"], len({e["repository"] for e in ENTRIES}))
        self.assertTrue(all(source["url"].startswith("https://github.com/") for source in sources["sources"]))

        for name in ("domains", "facets", "sources"):
            with self.subTest(file=name):
                document = published(build_data.V1_DIR / f"{name}.json")
                self.assertEqual(document["api_version"], build_data.API_VERSION)
                self.assertTrue(document[name if name != "facets" else "topics"])


class ApiCatalog(unittest.TestCase):
    """`/.well-known/api-catalog`, per RFC 9727 in the RFC 9264 linkset format."""

    def setUp(self):
        self.catalog = build_data.build_api_catalog()

    def test_is_a_linkset_anchored_on_its_own_url(self):
        contexts = self.catalog["linkset"]
        self.assertTrue(contexts)
        anchors = [context["anchor"] for context in contexts]
        self.assertIn(f"{build_data.SITE_URL}/{build_data.API_CATALOG_PATH.as_posix()}", anchors)
        self.assertIn(build_data.API_BASE_URL, anchors)

    def test_names_every_api_as_an_item(self):
        catalog_context = next(
            context
            for context in self.catalog["linkset"]
            if context["anchor"].endswith("api-catalog")
        )
        self.assertTrue(catalog_context["item"])
        self.assertEqual(catalog_context["item"][0]["href"], build_data.API_BASE_URL)
        self.assertIn("rfc9727", catalog_context["describedby"][0]["href"])

    def test_links_the_description_and_the_documentation_of_the_api(self):
        api = next(
            context
            for context in self.catalog["linkset"]
            if context["anchor"] == build_data.API_BASE_URL
        )
        self.assertEqual(
            api["service-desc"][0]["href"], f"{build_data.SITE_URL}/openapi.json"
        )
        docs = {link["href"] for link in api["service-doc"]}
        self.assertIn(build_data.API_DOCS_URL, docs)
        self.assertIn(build_data.DEVELOPERS_URL, docs)
        meta = {link["href"] for link in api["service-meta"]}
        self.assertIn(f"{build_data.API_BASE_URL}/version.json", meta)
        self.assertIn(f"{build_data.SITE_URL}/agents.md", meta)

    def test_published_file_agrees(self):
        self.assertEqual(published(build_data.API_CATALOG_PATH), self.catalog)

    def test_jekyll_is_told_to_publish_the_dot_directory(self):
        # Jekyll skips dot-directories, so the catalogue needs an explicit
        # include or it never reaches the site.
        config = (ROOT / "_config.yml").read_text(encoding="utf-8")
        self.assertRegex(config, r"include:\s*\n\s*-\s*\.well-known")


class AgentInstructions(unittest.TestCase):
    """`/agents.md`: what an agent reads before calling anything."""

    def setUp(self):
        self.text = build_data.build_agents(ENTRIES, DOMAINS)

    def test_says_when_to_use_it_and_when_not_to(self):
        self.assertIn("## When to use this", self.text)
        self.assertIn("## When not to use this", self.text)
        for item in build_data.WHEN_TO_USE:
            self.assertIn(item, self.text)
        for item in build_data.WHEN_NOT_TO_USE:
            self.assertIn(item, self.text)

    def test_names_the_calls_to_make(self):
        self.assertIn("## How to call it", self.text)
        for recipe in build_data.call_recipes():
            self.assertIn(recipe, self.text)
        self.assertIn(f"{build_data.API_BASE_URL}/index.json", self.text)

    def test_lists_the_domains_and_the_pacing(self):
        for domain in DOMAINS:
            self.assertIn(f"`{domain['slug']}`", self.text)
        self.assertIn("RateLimit-Policy", self.text)
        self.assertIn(str(build_data.RATE_LIMIT_QUOTA), self.text)

    def test_published_file_agrees(self):
        text = build_data.AGENTS_PATH.read_text(encoding="utf-8")
        self.assertTrue(text.startswith("# Awesome Reviewers — agent instructions"))
        self.assertIn("## When to use this", text)
        self.assertIn("## When not to use this", text)


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

    def test_says_when_to_use_the_corpus(self):
        self.assertIn("## When to use this", self.text)
        self.assertIn("/agents.md", self.text)

    def test_is_short_enough_to_be_worth_serving_as_the_homepage(self):
        # llms.txt lists every instruction; this is the one-screen version.
        self.assertLess(len(self.text), 9000)

    def test_published_file_agrees(self):
        text = (build_data.RAW_DIR / "site.md").read_text(encoding="utf-8")
        self.assertTrue(text.startswith("# Awesome Reviewers\n"))
        self.assertIn(f"{build_data.SITE_URL}/openapi.json", text)
        self.assertLess(len(text), 9000)


class LlmsTxt(unittest.TestCase):
    def setUp(self):
        self.text = "\n".join(build_data.build_llms(ENTRIES, DOMAINS))

    def test_names_the_api_and_lists_every_resource(self):
        self.assertIn("## Awesome Reviewers API — developer resources", self.text)
        for resource in build_data.DEV_RESOURCES:
            with self.subTest(resource=resource["name"]):
                self.assertIn(resource["name"], self.text)
                self.assertIn(f"{build_data.SITE_URL}{resource['path']}", self.text)

    def test_says_when_to_use_it_and_how_to_call_it(self):
        self.assertIn("## When to use Awesome Reviewers", self.text)
        self.assertIn("## When not to use it", self.text)
        self.assertIn("## How to call it", self.text)
        for item in build_data.WHEN_TO_USE:
            self.assertIn(item, self.text)

    def test_documents_the_error_format(self):
        self.assertIn("RFC 9457", self.text)
        for problem in build_data.build_problems():
            self.assertIn(problem["code"], self.text)
            self.assertIn(problem["type"], self.text)

    def test_documents_the_version_and_the_pacing(self):
        self.assertIn(f"{build_data.API_BASE_URL}/version.json", self.text)
        self.assertIn("RateLimit-Policy", self.text)

    def test_documents_the_markdown_variants(self):
        self.assertIn("/raw/<slug>.md", self.text)
        self.assertIn("/raw/bundles/<domain>.md", self.text)
        self.assertIn('rel="alternate"', self.text)

    def test_published_file_agrees(self):
        text = build_data.LLMS_PATH.read_text(encoding="utf-8")
        self.assertIn("## Awesome Reviewers API — developer resources", text)
        self.assertIn("## When to use Awesome Reviewers", text)
        self.assertIn(f"{build_data.SITE_URL}/openapi.json", text)


class NotFoundBody(unittest.TestCase):
    """The 404 body has to let an agent recover without a second guess."""

    def setUp(self):
        self.source = (ROOT / "404.html").read_text(encoding="utf-8")
        self.markdown = build_data.build_not_found_markdown()

    def test_is_published_at_the_path_github_pages_serves(self):
        self.assertIn("permalink: /404.html", self.source)

    def test_the_markdown_body_points_at_every_index(self):
        for target in (
            "/raw/index.json",
            f"{build_data.API_BASE}/index.json",
            "/llms.txt",
            "/agents.md",
            "/openapi.json",
            "/sitemap.xml",
            "/api/",
            "/developers/",
        ):
            with self.subTest(target=target):
                self.assertIn(target, self.markdown)

    def test_the_markdown_body_explains_the_path_shapes(self):
        self.assertTrue(self.markdown.startswith("# 404 Not Found"))
        self.assertIn("## Recover", self.markdown)
        self.assertIn("## Path shapes", self.markdown)
        self.assertIn("/raw/<slug>.md", self.markdown)

    def test_is_published_as_a_file_of_its_own(self):
        self.assertEqual(
            build_data.NOT_FOUND_PATH.read_text(encoding="utf-8"), self.markdown
        )

    def test_the_html_page_renders_the_same_markdown(self):
        # One text, three places: /404.md, the HTML page and the edge worker.
        self.assertIn("api.not_found_markdown", self.source)
        self.assertEqual(published(build_data.DATA_DIR / "api.json")["not_found_markdown"], self.markdown)

    def test_carries_the_problem_details_for_machines(self):
        self.assertIn('<script type="application/problem+json" id="problem">', self.source)
        self.assertIn('"status": 404', self.source)
        self.assertIn('"code": "not_found"', self.source)


class ProsePages(unittest.TestCase):
    """The trust anchors, and their markdown twins."""

    def pages(self):
        return {name: (ROOT / f"{name}.md") for name in build_data.PROSE_PAGES}

    def test_every_prose_page_exists_and_is_published_at_its_own_path(self):
        for name, path in self.pages().items():
            with self.subTest(page=name):
                self.assertTrue(path.exists(), f"{path} is missing")
                meta, _ = build_data.parse_front_matter(path.read_text(encoding="utf-8"))
                self.assertEqual(meta["permalink"], f"/{name}/")
                self.assertEqual(meta["layout"], "page")
                self.assertTrue(meta["title"])
                self.assertTrue(meta["description"])

    def test_each_page_carries_enough_content_to_be_worth_reading(self):
        for name, path in self.pages().items():
            with self.subTest(page=name):
                _, body = build_data.parse_front_matter(path.read_text(encoding="utf-8"))
                self.assertGreater(len(body), 1500, f"{name} is thin")

    def test_no_liquid_leaks_into_the_markdown_twin(self):
        for name, path in self.pages().items():
            with self.subTest(page=name):
                _, body = build_data.parse_front_matter(path.read_text(encoding="utf-8"))
                self.assertNotIn("{{", body)
                self.assertNotIn("{%", body)

    def test_the_twin_is_the_page_verbatim(self):
        for name, path in self.pages().items():
            with self.subTest(page=name):
                meta, body = build_data.parse_front_matter(path.read_text(encoding="utf-8"))
                twin = (build_data.RAW_DIR / f"{name}.md").read_text(encoding="utf-8")
                self.assertIn(f"url: {build_data.SITE_URL}/{name}/", twin)
                self.assertIn(f"# {meta['title']}", twin)
                self.assertIn(body, twin)

    def test_a_page_slug_cannot_be_taken_by_an_instruction(self):
        self.assertTrue(build_data.RESERVED_SLUGS.issuperset(build_data.PROSE_PAGES))
        instructions = {path.stem for path in build_data.REVIEWERS_DIR.glob("*.md")}
        self.assertEqual(build_data.RESERVED_SLUGS & instructions, set())

    def test_the_privacy_page_names_what_actually_runs_on_the_site(self):
        privacy = (ROOT / "privacy.md").read_text(encoding="utf-8")
        base = (ROOT / "_layouts" / "base.html").read_text(encoding="utf-8")
        site_js = (ROOT / "assets" / "js" / "site.js").read_text(encoding="utf-8")
        if "googletagmanager" in base:
            self.assertIn("Google Analytics", privacy)
        if "zi-scripts" in base or "ZIProjectKey" in base:
            self.assertIn("ZoomInfo", privacy)
        if "awesome.baz.co" in site_js:
            self.assertIn("awesome.baz.co", privacy)

    def test_the_developer_portal_covers_what_an_integrator_needs(self):
        portal = (ROOT / "developers.md").read_text(encoding="utf-8")
        for section in (
            "## Quickstart",
            "## Authentication",
            "## Versioning",
            "## Deprecation",
            "## Rate limits",
            "## Errors",
            "## CLI",
            "## Run it locally",
            "## Support",
        ):
            with self.subTest(section=section):
                self.assertIn(section, portal)
        self.assertIn(f'"{build_data.RATE_LIMIT_NAME}";q={build_data.RATE_LIMIT_QUOTA}', portal)
        self.assertIn(str(build_data.SUNSET_NOTICE_DAYS), portal)
        self.assertIn(build_data.CLI_PATH, portal)


class StructuredData(unittest.TestCase):
    """JSON-LD: the identity of the site, in a form a machine can read."""

    def setUp(self):
        self.graph = json_ld((ROOT / "index.html").read_text(encoding="utf-8"))

    def nodes(self):
        return [node for block in self.graph for node in block.get("@graph", [block])]

    def node(self, type_name):
        return next(node for node in self.nodes() if node["@type"] == type_name)

    def test_the_homepage_carries_parseable_json_ld(self):
        self.assertTrue(self.graph, "no JSON-LD on the homepage")
        for block in self.graph:
            self.assertEqual(block["@context"], "https://schema.org")

    def test_it_declares_the_site_the_dataset_and_the_api(self):
        types = {node["@type"] for node in self.nodes()}
        self.assertTrue({"WebSite", "Organization", "Dataset", "WebAPI"}.issubset(types))
        website = self.node("WebSite")
        self.assertEqual(website["name"], "Awesome Reviewers")
        self.assertTrue(website["description"])
        self.assertTrue(website["url"])
        self.assertEqual(website["publisher"]["@id"], self.node("Organization")["@id"])

    def test_the_organization_can_be_contacted_and_located(self):
        organization = self.node("Organization")
        self.assertTrue(organization["name"])
        self.assertTrue(organization["url"])
        self.assertTrue(organization["sameAs"])

        address = organization["address"]
        self.assertEqual(address["@type"], "PostalAddress")
        self.assertTrue(address["addressLocality"])
        self.assertTrue(address["addressCountry"])

        contacts = organization["contactPoint"]
        self.assertTrue(contacts)
        for contact in contacts:
            with self.subTest(contact=contact.get("contactType")):
                self.assertEqual(contact["@type"], "ContactPoint")
                self.assertTrue(contact["contactType"])
                self.assertTrue(contact.get("email") or contact.get("url"))
        self.assertTrue(any(contact.get("email") for contact in contacts), "no email anywhere")

    def test_the_dataset_says_where_to_download_it(self):
        dataset = self.node("Dataset")
        self.assertEqual(dataset["license"], "https://www.apache.org/licenses/LICENSE-2.0")
        self.assertTrue(dataset["isAccessibleForFree"])
        formats = {download["encodingFormat"] for download in dataset["distribution"]}
        self.assertIn("application/json", formats)
        self.assertIn("text/markdown", formats)

    def test_the_api_page_describes_the_api(self):
        api = json_ld((ROOT / "api.html").read_text(encoding="utf-8"))
        self.assertTrue(api)
        node = api[0]
        self.assertEqual(node["@type"], "WebAPI")
        self.assertEqual(node["name"], "Awesome Reviewers API")
        self.assertTrue(node["documentation"])
        provider = node["provider"]
        self.assertEqual(provider["address"]["@type"], "PostalAddress")
        self.assertTrue(provider["contactPoint"]["url"])


class DiscoveryLinks(unittest.TestCase):
    def setUp(self):
        self.base = (ROOT / "_layouts" / "base.html").read_text(encoding="utf-8")

    def test_every_page_advertises_the_openapi_description(self):
        self.assertIn('rel="service-desc"', self.base)
        self.assertIn("/openapi.json", self.base)
        self.assertIn('rel="service-doc"', self.base)

    def test_every_page_advertises_the_version_the_catalogue_and_the_instructions(self):
        self.assertIn('rel="service-meta"', self.base)
        self.assertIn("/v1/version.json", self.base)
        self.assertIn('rel="api-catalog"', self.base)
        self.assertIn("/.well-known/api-catalog", self.base)
        self.assertIn('rel="help"', self.base)
        self.assertIn("/agents.md", self.base)

    def test_pages_with_a_markdown_twin_advertise_it(self):
        self.assertIn('rel="alternate" type="text/markdown"', self.base)
        self.assertIn("'/raw/' | append: page.slug | append: '.md'", self.base)
        self.assertIn("'/raw/bundles/' | append: page.domain | append: '.md'", self.base)
        # Prose pages are authored as markdown, so they have twins too.
        self.assertIn("page.layout == 'page'", self.base)

    def test_instruction_pages_advertise_their_json(self):
        self.assertIn('rel="alternate" type="application/json"', self.base)
        self.assertIn("'/v1/instructions/' | append: page.slug | append: '.json'", self.base)

    def test_the_footer_links_the_trust_pages(self):
        for page in build_data.PROSE_PAGES:
            with self.subTest(page=page):
                self.assertIn(f"'/{page}/'", self.base)

    def test_robots_lists_every_concrete_developer_resource(self):
        robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
        self.assertIn("Sitemap: https://awesomereviewers.com/sitemap.xml", robots)
        for resource in build_data.DEV_RESOURCES:
            with self.subTest(path=resource["path"]):
                self.assertIn(resource["path"], robots)

    def test_api_page_is_discoverable_by_name(self):
        api_page = (ROOT / "api.html").read_text(encoding="utf-8")
        self.assertIn("<h1>Awesome Reviewers API</h1>", api_page)
        self.assertIn('"@type": "WebAPI"', api_page)
        self.assertIn('"name": "Awesome Reviewers API"', api_page)

    def test_api_page_documents_the_version_and_the_quota(self):
        api_page = (ROOT / "api.html").read_text(encoding="utf-8")
        for anchor in ('id="versioning"', 'id="rate-limits"', 'id="json"', 'id="discovery"'):
            with self.subTest(anchor=anchor):
                self.assertIn(anchor, api_page)
        self.assertIn("rfc9745", api_page)
        self.assertIn("rfc8594", api_page)
        self.assertIn("acceptmarkdown.com", api_page)


class Cli(unittest.TestCase):
    """The CLI is published from the site, so it is part of the interface."""

    def setUp(self):
        self.path = ROOT / build_data.CLI_PATH.lstrip("/")

    def test_is_published_where_the_resource_list_says_it_is(self):
        self.assertTrue(self.path.exists(), f"{self.path} is missing")
        self.assertIn(
            build_data.CLI_PATH,
            [resource["path"] for resource in build_data.DEV_RESOURCES],
        )

    def test_carries_no_front_matter_so_jekyll_serves_it_verbatim(self):
        self.assertFalse(self.path.read_text(encoding="utf-8").startswith("---"))

    def test_targets_the_documented_endpoints(self):
        # tests/test_cli.py asserts the URLs it builds against build_data; this
        # only checks that the published file is the one they describe.
        source = self.path.read_text(encoding="utf-8")
        self.assertIn(build_data.SITE_URL, source)
        self.assertIn(f'API_BASE = "{build_data.API_BASE}"', source)
        self.assertIn("/raw/bundles/", source)


class BuildHygiene(unittest.TestCase):
    def test_derived_artifacts_are_not_committed(self):
        ignored = (ROOT / ".gitignore").read_text(encoding="utf-8").split()
        for path in (
            "openapi.json",
            "_data/api.json",
            "llms.txt",
            "agents.md",
            "404.md",
            "v1/",
            ".well-known/",
        ):
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

    def test_the_generated_markdown_endpoints_carry_no_front_matter_either(self):
        for path in (build_data.AGENTS_PATH, build_data.NOT_FOUND_PATH):
            with self.subTest(path=str(path)):
                self.assertFalse(path.read_text(encoding="utf-8").startswith("---"))


if __name__ == "__main__":
    unittest.main()
