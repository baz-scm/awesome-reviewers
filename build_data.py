#!/usr/bin/env python3
"""Build every derived artifact the site and its machine consumers need.

Reads the source corpus in `_reviewers/` (one markdown instruction per file plus
a sibling JSON file holding the review discussions it was derived from) and
writes:

  _data/domains.json        domain definitions + per-domain stats
  _data/entries.json        one row per instruction, newest activity first
  _data/meta.json           slug -> derived metadata (O(1) lookup from Liquid)
  _data/sources.json        one row per source repository
  assets/data/search.json   compact index for client-side search
  raw/<slug>.md             plain-text endpoint for a single instruction
  raw/bundles/<domain>.md   every instruction in a domain, concatenated
  raw/index.json            machine-readable index of the whole corpus
  raw/verifications/        one scan per source repository, plus an index
  raw/verify/               per-language verification playbooks (.md, .json) and an index
  _data/verify.json         playbooks, methods and check kinds for the site layer
  _data/source_pages.json   one entry per source repository page
  verify/ methods/ sources/ thin page stubs the layouts render
  llms.txt                  domain-grouped index for LLM consumers
  openapi.json              OpenAPI 3.1 description of the endpoints above

Everything here is derived. Nothing outside `_reviewers/` and `_verifications/` is a source of truth,
so the script is safe to re-run at any time and is expected to run in CI before
`jekyll build`.
"""

from __future__ import annotations

import json
import os
import re
import shutil
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

REVIEWERS_DIR = Path("_reviewers")
VERIFICATIONS_DIR = Path("_verifications")
DATA_DIR = Path("_data")
RAW_DIR = Path("raw")
SEARCH_PATH = Path("assets/data/search.json")
LLMS_PATH = Path("llms.txt")
OPENAPI_PATH = Path("openapi.json")
SITE_URL = "https://awesomereviewers.com"
# Problem types are documented on the 404 page, one #error-<code> section each.
ERRORS_DOCS_URL = f"{SITE_URL}/404.html"
REPOSITORY_URL = "https://github.com/baz-scm/awesome-reviewers"
# Name of the site overview under raw/. No instruction may use it as a slug.
SITE_OVERVIEW_SLUG = "site"

# Slugs become file names, URLs and HTML/JSON/markdown text. Anything outside this
# shape (`#`, `?`, quotes, control characters, non-ASCII, over-long names) is
# rejected rather than escaped, so a malformed source can never reach the site.
SLUG_PATTERN = re.compile(r"[a-z0-9]+(?:[.-][a-z0-9]+)*")
SLUG_MAX_LENGTH = 100
REPOSITORY_PATTERN = re.compile(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+")


def slug_problem(slug: str) -> str | None:
    """Return why `slug` is not a valid instruction slug, or None if it is."""
    if len(slug) > SLUG_MAX_LENGTH:
        return f"longer than {SLUG_MAX_LENGTH} characters"
    if not SLUG_PATTERN.fullmatch(slug):
        return "must be lowercase ASCII letters and digits separated by '-' or '.'"
    return None


def validate_corpus_names(directory: Path) -> None:
    """Fail the build if any corpus file has a name or repository the site cannot carry."""
    problems: list[str] = []
    for path in sorted(directory.iterdir()):
        if path.suffix not in (".md", ".json"):
            problems.append(f"{path.name!r}: not a .md or .json file")
            continue
        reason = slug_problem(path.stem)
        if reason:
            problems.append(f"{path.name!r}: {reason}")
            continue
        if path.suffix == ".md":
            meta, _ = parse_front_matter(path.read_text(encoding="utf-8", errors="replace"))
            repo = meta.get("repository", "")
            if repo and not REPOSITORY_PATTERN.fullmatch(repo):
                problems.append(f"{path.name!r}: repository {repo!r} is not 'owner/name'")
    if problems:
        shown = "\n  ".join(problems[:50])
        more = f"\n  ... and {len(problems) - 50} more" if len(problems) > 50 else ""
        raise SystemExit(f"{len(problems)} invalid files in {directory}/:\n  {shown}{more}")

# --------------------------------------------------------------------------- #
# Domains
# --------------------------------------------------------------------------- #

DOMAINS: list[dict] = [
    {
        "slug": "ai-agents",
        "title": "AI Agents & Assistants",
        "blurb": "Agent loops, tool calling, prompt and context assembly, agent SDKs and coding assistants.",
    },
    {
        "slug": "llm-infra",
        "title": "LLM Serving & Gateways",
        "blurb": "Inference servers, model gateways and routers, KV caching, retrieval and ingestion pipelines.",
    },
    {
        "slug": "ml-systems",
        "title": "ML Frameworks & Platforms",
        "blurb": "Training and inference frameworks, tensor and kernel code, ML platforms and pipelines.",
    },
    {
        "slug": "orchestration",
        "title": "Containers & Orchestration",
        "blurb": "Kubernetes, schedulers, service meshes, container tooling, workflow and job engines.",
    },
    {
        "slug": "cloud-infra",
        "title": "Cloud, IaC & Networking",
        "blurb": "Infrastructure as code, cloud SDKs, edge runtimes, proxies, gateways and tunnels.",
    },
    {
        "slug": "data-systems",
        "title": "Databases & Data Platforms",
        "blurb": "Query engines, storage, replication, streaming, ORMs and analytics backends.",
    },
    {
        "slug": "observability",
        "title": "Observability & Telemetry",
        "blurb": "Metrics, tracing, logging, error tracking and instrumentation of production systems.",
    },
    {
        "slug": "security",
        "title": "Security & Access Control",
        "blurb": "Static analysis, cloud posture scanning, authentication, authorization and secrets handling.",
    },
    {
        "slug": "runtimes",
        "title": "Language Runtimes & Compilers",
        "blurb": "Interpreters, compilers, async runtimes, parsers and low-level systems code.",
    },
    {
        "slug": "devtools",
        "title": "Developer Tooling",
        "blurb": "Editors, terminals, build systems, package managers, linters, formatters and test runners.",
    },
    {
        "slug": "app-frameworks",
        "title": "Application Frameworks & UI",
        "blurb": "Web and mobile frameworks, component libraries, API layers and product codebases.",
    },
    {
        "slug": "docs",
        "title": "Documentation & Knowledge",
        "blurb": "Reference material, curated lists and learning resources — mostly writing and structure guidance.",
    },
]

DOMAIN_SLUGS = [d["slug"] for d in DOMAINS]

# Explicit repository -> domain assignment. Keyed by lowercased `owner/repo`.
REPO_DOMAIN: dict[str, str] = {}


def _assign(domain: str, repos: str) -> None:
    for repo in repos.split():
        REPO_DOMAIN[repo.lower()] = domain


_assign("ai-agents", """
    aider-ai/aider qwenlm/qwen-code roocodeinc/roo-code swe-agent/swe-agent
    tauricresearch/tradingagents agent0ai/agent-zero aaif-goose/goose block/goose
    anthropics/claude-code anthropics/claude-agent-sdk-python anthropics/anthropic-sdk-python
    browser-use/browser-use browserbase/stagehand bytedance/ui-tars-desktop
    bytedance/deer-flow bytedance/trae-agent cline/cline cloudflare/agents
    coleam00/archon continuedev/continue crewaiinc/crewai dyad-sh/dyad
    earendil-works/pi emcie-co/parlant google-gemini/gemini-cli google-gemini/gemini-skills
    kilo-org/kilocode nousresearch/hermes-agent openai/codex openai/skills openai/openai-python
    oraios/serena ruvnet/ruflo smallcloudai/refact sst/opencode stanfordnlp/dspy
    strands-agents/sdk-python vercel/ai vercel-labs/agent-skills n8n-io/n8n
    langchain-ai/langchain langchain-ai/langchainjs langflow-ai/langflow
    lobehub/lobe-chat chatgptnextweb/nextchat chatgptbox-dev/chatgptbox
    hmbown/deepseek-tui firecrawl/firecrawl eosphoros-ai/db-gpt
""")

_assign("llm-infra", """
    vllm-project/vllm sgl-project/sglang ggml-org/llama.cpp ollama/ollama
    berriai/litellm maximhq/bifrost lmcache/lmcache diegosouzapw/omniroute
    looplj/axonhub decolua/9router langgenius/dify infiniflow/ragflow
    menloresearch/jan unstructured-io/unstructured microsoft/markitdown
""")

_assign("ml-systems", """
    pytorch/pytorch tensorflow/tensorflow tensorflow/swift apache/mxnet
    deeplearning4j/deeplearning4j tencent/ncnn opencv/opencv huggingface/tokenizers
    qwenlm/qwen3 karpathy/nanochat p-e-w/heretic comfyanonymous/comfyui
    kubeflow/kubeflow commaai/openpilot
""")

_assign("orchestration", """
    kubernetes/kubernetes argoproj/argo-cd volcano-sh/volcano istio/istio
    docker/compose wagoodman/dive temporalio/temporal apache/airflow celery/celery
""")

_assign("cloud-infra", """
    hashicorp/terraform opentofu/opentofu chef/chef serverless/serverless
    cloudflare/workerd cloudflare/workers-sdk aws/aws-sdk-js boto/boto3
    azure/azure-sdk-for-net traefik/traefik kong/kong apache/apisix
    fatedier/frp unionlabs/union
""")

_assign("data-systems", """
    clickhouse/clickhouse duckdb/duckdb neondatabase/neon redis/redis
    elastic/elasticsearch influxdata/influxdb apache/kafka apache/spark
    vitessio/vitess prisma/prisma drizzle-team/drizzle-orm supabase/supabase
    pola-rs/polars posthog/posthog rocicorp/mono
""")

_assign("observability", """
    grafana/grafana prometheus/prometheus signoz/signoz getsentry/sentry
    getsentry/sentry-php open-telemetry/opentelemetry-python langfuse/langfuse
""")

_assign("security", """
    bridgecrewio/checkov prowler-cloud/prowler semgrep/semgrep opengrep/opengrep
    snyk/cli gravitational/teleport salesforce/cloudsplaining better-auth/better-auth
""")

_assign("runtimes", """
    denoland/deno oven-sh/bun nodejs/node golang/go rust-lang/rust
    llvm/llvm-project tokio-rs/tokio netty/netty jetbrains/kotlin
    microsoft/typescript vlang/v servo/servo tree-sitter/tree-sitter
    torvalds/linux bytedance/sonic facebook/yoga dotnet/runtime
""")

_assign("devtools", """
    microsoft/vscode zed-industries/zed neovim/neovim helix-editor/helix
    alacritty/alacritty ghostty-org/ghostty microsoft/terminal warpdotdev/warp
    wavetermdev/waveterm jj-vcs/jj homebrew/brew bazelbuild/bazel nrwl/nx
    vercel/turborepo vitejs/vite prettier/prettier astral-sh/ruff astral-sh/ty
    astral-sh/uv python-poetry/poetry microsoft/playwright cypress-io/cypress
    mermaid-js/mermaid likec4/likec4 evanw/esbuild electron/electron
    mountain-loop/yaak octokit/octokit.net zen-browser/desktop hyprwm/hyprland
""")

_assign("app-frameworks", """
    facebook/react facebook/react-native vercel/next.js angular/angular vuejs/core
    sveltejs/svelte nuxt/nuxt remix-run/react-router tanstack/router tanstack/query
    mui/material-ui ant-design/ant-design shadcn-ui/ui flutter/flutter
    django/django rails/rails laravel/framework spring-projects/spring-boot
    spring-projects/spring-framework fastapi/fastapi expressjs/express
    fastify/fastify gin-gonic/gin gofiber/fiber nestjs/nest adonisjs/core
    tokio-rs/axum axios/axios colinhacks/zod pydantic/pydantic quarkusio/quarkus
    vadimdemedes/ink mastodon/mastodon discourse/discourse calcom/cal.com
    twentyhq/twenty novuhq/novu home-assistant/core appwrite/appwrite
    elie222/inbox-zero maplibre/maplibre-native logseq/logseq juspay/hyperswitch
""")

_assign("docs", """
    ebookfoundation/free-programming-books kamranahmedse/developer-roadmap
    freecodecamp/freecodecamp avelino/awesome-go ossu/computer-science
    thealgorithms/python
""")

# Fallback for repositories added to the corpus after this map was written.
# Ordered: the first matching pattern wins.
FALLBACK_RULES: list[tuple[str, str]] = [
    (r"agent|copilot|assistant|\bllm\b|chat|prompt|skills|mcp", "ai-agents"),
    (r"infer|serving|gateway|router|rag|embed|tokeni", "llm-infra"),
    (r"torch|tensor|\bml\b|train|model|diffus|cuda|kernel", "ml-systems"),
    (r"kube|k8s|container|docker|helm|mesh|scheduler|workflow|airflow", "orchestration"),
    (r"terraform|tofu|cloud|aws|azure|gcp|serverless|proxy|ingress|network", "cloud-infra"),
    (r"\bdb\b|sql|database|stream|kafka|warehouse|orm|storage", "data-systems"),
    (r"metric|trace|telemetr|monitor|logging|observ", "observability"),
    (r"secur|auth|scan|vuln|secret|policy", "security"),
    (r"compil|runtime|parser|lang|interpret", "runtimes"),
    (r"lint|format|build|bundler|editor|terminal|test|cli", "devtools"),
]

LABEL_DOMAIN_HINTS: dict[str, str] = {
    "ai": "ai-agents",
    "security": "security",
    "observability": "observability",
    "logging": "observability",
    "database": "data-systems",
    "migrations": "data-systems",
    "ci/cd": "orchestration",
    "configurations": "cloud-infra",
    "networking": "cloud-infra",
    "documentation": "docs",
    "react": "app-frameworks",
    "vue": "app-frameworks",
    "angular": "app-frameworks",
    "next": "app-frameworks",
    "pytorch": "ml-systems",
}


def classify(repo: str, label: str) -> str:
    """Return the domain slug for a corpus entry."""
    key = repo.lower()
    if key in REPO_DOMAIN:
        return REPO_DOMAIN[key]
    for pattern, domain in FALLBACK_RULES:
        if re.search(pattern, key):
            return domain
    return LABEL_DOMAIN_HINTS.get(label.lower(), "app-frameworks")


# --------------------------------------------------------------------------- #
# Corpus reading
# --------------------------------------------------------------------------- #

FRONT_MATTER_RE = re.compile(r"\A---\n(.*?)\n---\n?(.*)\Z", re.DOTALL)
SCALAR_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*):\s*(.*)$")


def parse_front_matter(text: str) -> tuple[dict[str, str], str]:
    """Parse the flat front matter used across the corpus, plus the body.

    The corpus front matter is deliberately flat (string and integer scalars,
    some of them wrapped over continuation lines), so a small parser keeps this
    script dependency-free instead of pulling in PyYAML.
    """
    match = FRONT_MATTER_RE.match(text)
    if not match:
        return {}, text.strip()

    meta: dict[str, str] = {}
    key = None
    for line in match.group(1).split("\n"):
        scalar = SCALAR_RE.match(line)
        if scalar:
            key = scalar.group(1)
            meta[key] = scalar.group(2).strip()
        elif key and line.startswith((" ", "\t")):
            meta[key] = f"{meta[key]} {line.strip()}".strip()
    return {k: unquote(v) for k, v in meta.items()}, match.group(2).strip()


def unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1].strip()
    return value


def as_int(value: str | None) -> int:
    try:
        return int(str(value).strip())
    except (TypeError, ValueError):
        return 0


def read_discussions(path: Path) -> tuple[list[str], int, int, list[str]]:
    """Return (sorted timestamps, thread count, comment count, comment authors)."""
    if not path.exists():
        return [], 0, 0, []
    try:
        with path.open(encoding="utf-8") as handle:
            discussions = json.load(handle)
    except (json.JSONDecodeError, OSError):
        return [], 0, 0, []

    if not isinstance(discussions, list):
        return [], 0, 0, []

    stamps: list[str] = []
    authors: list[str] = []
    comments = 0
    for discussion in discussions:
        if discussion.get("created_at"):
            stamps.append(str(discussion["created_at"]))
        for comment in discussion.get("discussion_comments") or []:
            comments += 1
            if comment.get("comment_created_at"):
                stamps.append(str(comment["comment_created_at"]))
            if comment.get("comment_author"):
                authors.append(str(comment["comment_author"]))
    return sorted(stamps), len(discussions), comments, authors


def day(stamp: str | None) -> str:
    return stamp[:10] if stamp else ""


def read_corpus() -> list[dict]:
    entries: list[dict] = []
    unmapped: Counter[str] = Counter()
    validate_corpus_names(REVIEWERS_DIR)

    for md_path in sorted(REVIEWERS_DIR.glob("*.md")):
        slug = md_path.stem
        text = md_path.read_text(encoding="utf-8", errors="replace")
        meta, body = parse_front_matter(text)
        if not meta.get("title"):
            continue

        repo = meta.get("repository", "")
        label = meta.get("label", "")
        stamps, threads, comment_count, authors = read_discussions(md_path.with_suffix(".json"))
        if repo and repo.lower() not in REPO_DOMAIN:
            unmapped[repo] += 1

        entries.append(
            {
                "slug": slug,
                "title": meta["title"],
                "description": meta.get("description", ""),
                "repository": repo,
                "topic": label,
                "language": meta.get("language", ""),
                "domain": classify(repo, label),
                "comments": as_int(meta.get("comments_count")) or comment_count,
                "stars": as_int(meta.get("repository_stars")),
                "discussions": threads,
                "updated": day(stamps[-1] if stamps else None),
                "first_seen": day(stamps[0] if stamps else None),
                "authors": sorted(set(authors)),
                "body": body,
            }
        )

    if unmapped:
        print(f"note: {len(unmapped)} repositories fell back to heuristic classification:")
        for repo, count in unmapped.most_common():
            print(f"  {repo} ({count} entries) -> {classify(repo, '')}")
    return entries


# --------------------------------------------------------------------------- #
# Verifications: the checks each source repository runs, one scan per repository
# --------------------------------------------------------------------------- #

# Mirrors `VerificationMethod` and `Trigger` in bazai's
# `modes/awesome_reviewers/verifications/models.py`, which writes these files.
VERIFICATION_METHODS: list[dict] = [
    {"slug": "formal", "title": "Formal verification and model checking"},
    {"slug": "static_analysis", "title": "Static analysis"},
    {"slug": "testing", "title": "Testing"},
    {"slug": "formatting", "title": "Formatting and hygiene"},
    {"slug": "supply_chain", "title": "Supply chain"},
    {"slug": "unclassified", "title": "Unclassified"},
]
VERIFICATION_METHOD_SLUGS = [m["slug"] for m in VERIFICATION_METHODS]
VERIFICATION_TRIGGERS = ["pre_commit", "ci", "local"]
URL_PATTERN = re.compile(r"https://[^\s\"'<>]+")


def repository_slug(repo: str) -> str:
    """`owner/name` as a file name: `pallets/flask` -> `pallets-flask`."""
    return re.sub(r"[^a-z0-9.]+", "-", repo.lower()).strip("-.")


def _text_list(value: object, field: str, problems: list[str]) -> list[str]:
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        problems.append(f"{field} must be a list of strings")
        return []
    return value


def _url(value: object, field: str, problems: list[str]) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str) or not URL_PATTERN.fullmatch(value):
        problems.append(f"{field} must be an https URL")
        return None
    return value


def normalize_verification(raw: object, where: str, problems: list[str]) -> dict | None:
    if not isinstance(raw, dict):
        problems.append(f"{where}: not an object")
        return None
    local: list[str] = []
    tool = raw.get("tool")
    method = raw.get("method")
    if tool is not None and not (isinstance(tool, str) and SLUG_PATTERN.fullmatch(tool)):
        local.append("tool must be null or a lowercase slug")
    if method not in VERIFICATION_METHOD_SLUGS:
        local.append(f"method {method!r} is not one of {VERIFICATION_METHOD_SLUGS}")
    triggers = _text_list(raw.get("triggers", []), "triggers", local)
    if any(trigger not in VERIFICATION_TRIGGERS for trigger in triggers):
        local.append(f"triggers must be drawn from {VERIFICATION_TRIGGERS}")
    evidence = raw.get("evidence", [])
    if not isinstance(evidence, list) or not all(
        isinstance(item, dict) and isinstance(item.get("path"), str) and isinstance(item.get("locator"), str)
        for item in evidence
    ):
        local.append("evidence must be a list of {path, locator}")
        evidence = []
    exit_codes = raw.get("exit_codes", {})
    if not isinstance(exit_codes, dict) or not all(
        str(code).lstrip("-").isdigit() and isinstance(meaning, str) for code, meaning in exit_codes.items()
    ):
        local.append("exit_codes must map integer codes to strings")
        exit_codes = {}
    for flag in ("autofix", "declared_only"):
        if not isinstance(raw.get(flag, False), bool):
            local.append(f"{flag} must be a boolean")
    verification = {
        "tool": tool,
        "method": method,
        "commands": _text_list(raw.get("commands", []), "commands", local),
        "triggers": triggers,
        "evidence": [{"path": item["path"], "locator": item["locator"]} for item in evidence],
        "upstream": _url(raw.get("upstream"), "upstream", local),
        "docs": _url(raw.get("docs"), "docs", local),
        "exit_codes": {str(code): meaning for code, meaning in exit_codes.items()},
        "autofix": raw.get("autofix", False) is True,
        "declared_only": raw.get("declared_only", False) is True,
    }
    problems.extend(f"{where}: {problem}" for problem in local)
    return None if local else verification


def read_verifications(directory: Path = VERIFICATIONS_DIR) -> dict[str, dict]:
    """Read every scan in `directory`, keyed by repository. Fail the build on a malformed one."""
    if not directory.is_dir():
        return {}
    scans: dict[str, dict] = {}
    problems: list[str] = []
    for path in sorted(directory.iterdir()):
        if path.suffix != ".json":
            problems.append(f"{path.name!r}: not a .json file")
            continue
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError) as error:
            problems.append(f"{path.name!r}: invalid JSON ({error})")
            continue
        repo = raw.get("repo_full_name") if isinstance(raw, dict) else None
        if not isinstance(repo, str) or not REPOSITORY_PATTERN.fullmatch(repo):
            problems.append(f"{path.name!r}: repo_full_name {repo!r} is not 'owner/name'")
            continue
        if reason := slug_problem(path.stem):
            problems.append(f"{path.name!r}: {reason}")
            continue
        if path.stem != repository_slug(repo):
            problems.append(f"{path.name!r}: must be named {repository_slug(repo)}.json for {repo}")
            continue
        ref = raw.get("ref")
        if not isinstance(ref, str) or not re.fullmatch(r"[0-9a-f]{7,40}", ref):
            problems.append(f"{path.name!r}: ref must be a commit sha")
            continue
        items = raw.get("verifications")
        if not isinstance(items, list):
            problems.append(f"{path.name!r}: verifications must be a list")
            continue
        verifications = [
            verification
            for index, item in enumerate(items)
            if (verification := normalize_verification(item, f"{path.name!r} verifications[{index}]", problems))
        ]
        scans[repo] = {
            "repository": repo,
            "slug": path.stem,
            "ref": ref,
            "verifications": verifications,
        }
    if problems:
        shown = "\n  ".join(problems[:50])
        more = f"\n  ... and {len(problems) - 50} more" if len(problems) > 50 else ""
        raise SystemExit(f"invalid verification scans in {directory}/:\n  {shown}{more}")
    return scans


def verification_summary(scan: dict) -> dict:
    counts = Counter(v["method"] for v in scan["verifications"])
    return {
        "repository": scan["repository"],
        "ref": scan["ref"],
        "count": len(scan["verifications"]),
        "methods": {slug: counts[slug] for slug in VERIFICATION_METHOD_SLUGS if counts[slug]},
        "tools": sorted({v["tool"] for v in scan["verifications"] if v["tool"]}),
        "url": f"{SITE_URL}/raw/verifications/{scan['slug']}.json",
    }


# --------------------------------------------------------------------------- #
# Verification guide: which checks to run for the code being written
#
# Two sources of truth meet here. `_verifications/` says which checks the
# source repositories actually run; `_reviewers/` holds the review prompts for
# what those checks miss. The tables below are the editorial layer that joins
# them: what each tool is for, which languages it applies to, and which checks
# a kind of change calls for. Everything else is counted from the data.
# --------------------------------------------------------------------------- #

# What each method is for, keyed by the scanner's method slugs.
METHOD_GUIDE: dict[str, dict] = {
    "static_analysis": {
        "slug": "static-analysis",
        "summary": "Reads the code without running it: linters, type checkers, security and workflow scanners.",
        "when": "On every change. Cheapest signal, runs in seconds, and most findings point at an exact line.",
    },
    "testing": {
        "slug": "testing",
        "summary": "Runs the code: unit and integration tests, browser tests, property-based tests, fuzzing, mutation testing.",
        "when": (
            "On every change that alters behaviour. Add generated inputs (property tests, fuzzing) when the "
            "code parses, transforms or computes, and mutation testing when the tests themselves change."
        ),
    },
    "formatting": {
        "slug": "formatting",
        "summary": "Normalises layout, spelling and file hygiene so the diff only shows what changed.",
        "when": "On every change, before anything else. Almost always autofixable: run the fix, then commit.",
    },
    "supply_chain": {
        "slug": "supply-chain",
        "summary": "Checks dependencies: known vulnerabilities, disallowed licenses, lockfiles that disagree with manifests.",
        "when": "When a manifest or lockfile changes, and on a schedule, since advisories arrive after the code ships.",
    },
    "formal": {
        "slug": "formal",
        "summary": "Proves or exhaustively explores properties: model checking, proofs, undefined-behaviour interpreters.",
        "when": (
            "When a bug would be a memory-safety violation or an interleaving that tests are unlikely to hit: "
            "unsafe code, lock-free structures, consensus and protocol logic."
        ),
    },
}
GUIDE_METHODS = [slug for slug in VERIFICATION_METHOD_SLUGS if slug in METHOD_GUIDE]

# A kind of check: narrower than a method, and what a recommendation is made of.
CHECK_KINDS: list[dict] = [
    {"slug": "formatting", "title": "Formatting", "method": "formatting",
     "catches": "Layout drift that buries the real change in the diff."},
    {"slug": "file-hygiene", "title": "File hygiene", "method": "formatting",
     "catches": "Invalid JSON, YAML or TOML, merge markers, trailing whitespace, oversized files."},
    {"slug": "spelling", "title": "Spelling", "method": "formatting",
     "catches": "Typos in identifiers, comments and docs."},
    {"slug": "linting", "title": "Linting", "method": "static_analysis",
     "catches": "Bug-prone patterns, unused code and conventions the formatter does not cover."},
    {"slug": "type-checking", "title": "Type checking", "method": "static_analysis",
     "catches": "Wrong types, unhandled null or None, call signatures broken across modules."},
    {"slug": "security-scanning", "title": "Security scanning", "method": "static_analysis",
     "catches": "Injection, unsafe APIs and tainted data reaching a sink."},
    {"slug": "secret-scanning", "title": "Secret scanning", "method": "static_analysis",
     "catches": "Credentials and tokens committed to the repository."},
    {"slug": "workflow-linting", "title": "CI workflow linting", "method": "static_analysis",
     "catches": "Broken GitHub Actions syntax, script injection, over-broad token permissions."},
    {"slug": "docs-build", "title": "Docs build", "method": "static_analysis",
     "catches": "Broken cross-references, links and markup in documentation."},
    {"slug": "unit-tests", "title": "Unit and integration tests", "method": "testing",
     "catches": "Behaviour regressions on the paths the tests exercise."},
    {"slug": "browser-tests", "title": "End-to-end browser tests", "method": "testing",
     "catches": "User flows broken across components, routing and the network."},
    {"slug": "property-tests", "title": "Property-based tests", "method": "testing",
     "catches": "Edge-case inputs nobody wrote a test for; invariants over generated data."},
    {"slug": "fuzzing", "title": "Fuzzing", "method": "testing",
     "catches": "Crashes, panics and hangs on malformed input, especially in parsers and decoders."},
    {"slug": "mutation-testing", "title": "Mutation testing", "method": "testing",
     "catches": "Tests that keep passing whatever the code does."},
    {"slug": "version-matrix", "title": "Version and platform matrix", "method": "testing",
     "catches": "Breakage on a runtime version, OS or feature combination you did not run locally."},
    {"slug": "dependency-audit", "title": "Dependency audit", "method": "supply_chain",
     "catches": "Known-vulnerable or disallowed dependencies and licenses."},
    {"slug": "lockfile-check", "title": "Lockfile consistency", "method": "supply_chain",
     "catches": "A lockfile that no longer matches its manifest."},
    {"slug": "ub-detection", "title": "Undefined-behaviour detection", "method": "formal",
     "catches": "Memory-safety and aliasing violations in unsafe code."},
    {"slug": "concurrency-model-checking", "title": "Concurrency model checking", "method": "formal",
     "catches": "Races and orderings that fail only under specific interleavings."},
    {"slug": "proofs", "title": "Proofs and specifications", "method": "formal",
     "catches": "Design-level bugs in protocols and algorithms, checked against a specification."},
]
CHECK_KIND_SLUGS = [k["slug"] for k in CHECK_KINDS]
ANY_LANGUAGE = "*"

# Languages a playbook is published for. `entry_languages` are the `language`
# values in `_reviewers/` front matter that count as this language.
LANGUAGES: list[dict] = [
    {"slug": "python", "title": "Python", "entry_languages": ["Python"], "extensions": [".py", ".pyi"]},
    {"slug": "typescript", "title": "TypeScript", "entry_languages": ["TypeScript", "TSX"],
     "extensions": [".ts", ".tsx", ".mts", ".cts"]},
    {"slug": "javascript", "title": "JavaScript", "entry_languages": ["JavaScript"],
     "extensions": [".js", ".jsx", ".mjs", ".cjs"]},
    {"slug": "rust", "title": "Rust", "entry_languages": ["Rust"], "extensions": [".rs"]},
    {"slug": "go", "compiled": True, "title": "Go", "entry_languages": ["Go"], "extensions": [".go"]},
    {"slug": "java", "compiled": True, "title": "Java", "entry_languages": ["Java"], "extensions": [".java"]},
    {"slug": "kotlin", "compiled": True, "title": "Kotlin", "entry_languages": ["Kotlin"], "extensions": [".kt", ".kts"]},
    {"slug": "swift", "compiled": True, "title": "Swift", "entry_languages": ["Swift"], "extensions": [".swift"]},
    {"slug": "cpp", "compiled": True, "title": "C++", "entry_languages": ["C++"],
     "extensions": [".cc", ".cpp", ".cxx", ".hh", ".hpp", ".hxx"]},
    {"slug": "c", "compiled": True, "title": "C", "entry_languages": ["C"], "extensions": [".c", ".h"]},
    {"slug": "csharp", "compiled": True, "title": "C#", "entry_languages": ["C#"], "extensions": [".cs"]},
    {"slug": "ruby", "title": "Ruby", "entry_languages": ["Ruby"], "extensions": [".rb"]},
    {"slug": "php", "title": "PHP", "entry_languages": ["PHP"], "extensions": [".php"]},
    {"slug": "shell", "title": "Shell", "entry_languages": ["Shell"], "extensions": [".sh", ".bash", ".zsh"]},
    {"slug": "sql", "title": "SQL", "entry_languages": ["Sql"], "extensions": [".sql"]},
    {"slug": "yaml", "title": "YAML and CI workflows", "entry_languages": ["Yaml"], "extensions": [".yml", ".yaml"]},
    {"slug": "config", "title": "JSON and TOML", "entry_languages": ["Json", "Toml"], "extensions": [".json", ".toml"]},
    {"slug": "dockerfile", "title": "Dockerfile", "entry_languages": ["Dockerfile"],
     "extensions": ["Dockerfile", ".dockerfile"]},
    {"slug": "docs", "title": "Markdown and docs", "entry_languages": ["Markdown", "Txt"],
     "extensions": [".md", ".mdx", ".rst", ".txt"]},
]
LANGUAGE_SLUGS = [language["slug"] for language in LANGUAGES]
JS_TS = ["javascript", "typescript"]

# What each tool the scanner recognises is for. Its method, docs, upstream and
# exit codes come from the scans themselves.
TOOL_PROFILES: dict[str, dict] = {
    "ruff-check": {"kind": "linting", "languages": ["python"]},
    "ruff-format": {"kind": "formatting", "languages": ["python"]},
    "black": {"kind": "formatting", "languages": ["python"]},
    "isort": {"kind": "formatting", "languages": ["python"]},
    "flake8": {"kind": "linting", "languages": ["python"]},
    "pylint": {"kind": "linting", "languages": ["python"]},
    "mypy": {"kind": "type-checking", "languages": ["python"]},
    "pyright": {"kind": "type-checking", "languages": ["python"]},
    "pytest": {"kind": "unit-tests", "languages": ["python"]},
    "unittest": {"kind": "unit-tests", "languages": ["python"]},
    "hypothesis": {"kind": "property-tests", "languages": ["python"]},
    "mutmut": {"kind": "mutation-testing", "languages": ["python"]},
    "bandit": {"kind": "security-scanning", "languages": ["python"]},
    "pip-audit": {"kind": "dependency-audit", "languages": ["python"]},
    "uv-lock": {"kind": "lockfile-check", "languages": ["python"]},
    "sphinx": {"kind": "docs-build", "languages": ["python", "docs"]},
    "mkdocs": {"kind": "docs-build", "languages": ["python", "docs"]},
    "eslint": {"kind": "linting", "languages": JS_TS},
    "biome": {"kind": "linting", "languages": [*JS_TS, "config"]},
    "prettier": {"kind": "formatting", "languages": [*JS_TS, "yaml", "config", "docs"]},
    "tsc": {"kind": "type-checking", "languages": ["typescript"]},
    "jest": {"kind": "unit-tests", "languages": JS_TS},
    "vitest": {"kind": "unit-tests", "languages": JS_TS},
    "mocha": {"kind": "unit-tests", "languages": JS_TS},
    "node-test": {"kind": "unit-tests", "languages": JS_TS},
    "playwright": {"kind": "browser-tests", "languages": JS_TS},
    "fast-check": {"kind": "property-tests", "languages": JS_TS},
    "stryker": {"kind": "mutation-testing", "languages": JS_TS},
    "npm-audit": {"kind": "dependency-audit", "languages": JS_TS},
    "go-test": {"kind": "unit-tests", "languages": ["go"]},
    "go-vet": {"kind": "linting", "languages": ["go"]},
    "gofmt": {"kind": "formatting", "languages": ["go"]},
    "golangci-lint": {"kind": "linting", "languages": ["go"]},
    "staticcheck": {"kind": "linting", "languages": ["go"]},
    "govulncheck": {"kind": "dependency-audit", "languages": ["go"]},
    "cargo-test": {"kind": "unit-tests", "languages": ["rust"]},
    "cargo-check": {"kind": "type-checking", "languages": ["rust"]},
    "cargo-hack": {"kind": "version-matrix", "languages": ["rust"]},
    "clippy": {"kind": "linting", "languages": ["rust"]},
    "rustfmt": {"kind": "formatting", "languages": ["rust"]},
    "miri": {"kind": "ub-detection", "languages": ["rust"]},
    "loom": {"kind": "concurrency-model-checking", "languages": ["rust"]},
    "kani": {"kind": "proofs", "languages": ["rust"]},
    "proptest": {"kind": "property-tests", "languages": ["rust"]},
    "cargo-fuzz": {"kind": "fuzzing", "languages": ["rust"]},
    "cargo-mutants": {"kind": "mutation-testing", "languages": ["rust"]},
    "cargo-deny": {"kind": "dependency-audit", "languages": ["rust"]},
    "cargo-audit": {"kind": "dependency-audit", "languages": ["rust"]},
    "shellcheck": {"kind": "linting", "languages": ["shell"]},
    "actionlint": {"kind": "workflow-linting", "languages": ["yaml"]},
    "zizmor": {"kind": "workflow-linting", "languages": ["yaml"]},
    "tla-plus": {"kind": "proofs", "languages": [ANY_LANGUAGE]},
    "coq": {"kind": "proofs", "languages": [ANY_LANGUAGE]},
    "lean": {"kind": "proofs", "languages": [ANY_LANGUAGE]},
    "dafny": {"kind": "proofs", "languages": [ANY_LANGUAGE]},
    "codeql": {"kind": "security-scanning", "languages": [ANY_LANGUAGE]},
    "semgrep": {"kind": "security-scanning", "languages": [ANY_LANGUAGE]},
    "gitleaks": {"kind": "secret-scanning", "languages": [ANY_LANGUAGE]},
    "codespell": {"kind": "spelling", "languages": [ANY_LANGUAGE]},
    "pre-commit-hooks": {"kind": "file-hygiene", "languages": [ANY_LANGUAGE]},
    "dependency-review": {"kind": "dependency-audit", "languages": [ANY_LANGUAGE]},
    "ci-matrix": {"kind": "version-matrix", "languages": [ANY_LANGUAGE]},
}

# What the change touches -> the checks it calls for and the prompt topics that
# cover what those checks miss. The first entry is the baseline for every change.
# Every topic in the corpus must appear in exactly one entry (a test enforces it).
CHANGES: list[dict] = [
    {"slug": "every-change", "title": "Any change",
     "kinds": ["formatting", "linting", "type-checking", "unit-tests"],
     "topics": ["Code Style", "Naming Conventions"]},
    {"slug": "security", "title": "Authentication, input handling, secrets, permissions",
     "kinds": ["security-scanning", "secret-scanning", "dependency-audit"],
     "topics": ["Security"]},
    {"slug": "interfaces", "title": "Public APIs, signatures, error paths, nullability",
     "kinds": ["type-checking", "unit-tests", "property-tests"],
     "topics": ["API", "Error Handling", "Null Handling"]},
    {"slug": "services", "title": "Service and framework code",
     "kinds": ["unit-tests", "version-matrix"],
     "topics": ["Fastify", "NestJS", "Spring", "Axum", "Celery", "Temporal"]},
    {"slug": "algorithms", "title": "Algorithms, parsers, data transforms",
     "kinds": ["property-tests", "fuzzing", "mutation-testing", "proofs"],
     "topics": ["Algorithms"]},
    {"slug": "concurrency", "title": "Threads, async code, locks, shared state",
     "kinds": ["concurrency-model-checking", "ub-detection", "property-tests"],
     "topics": ["Concurrency"]},
    {"slug": "networking", "title": "Network calls, retries, timeouts, protocols",
     "kinds": ["unit-tests", "fuzzing"],
     "topics": ["Networking", "Axios"]},
    {"slug": "ui", "title": "UI components and pages",
     "kinds": ["browser-tests", "linting"],
     "topics": ["React", "Next", "Next.js", "Vue", "Angular"]},
    {"slug": "data", "title": "Databases, migrations, caching",
     "kinds": ["unit-tests", "version-matrix"],
     "topics": ["Database", "Migrations", "Caching"]},
    {"slug": "performance", "title": "Hot paths and performance",
     "kinds": [],
     "topics": ["Performance Optimization"]},
    {"slug": "ai", "title": "Model, prompt and LLM code",
     "kinds": ["unit-tests"],
     "topics": ["AI", "Pytorch"]},
    {"slug": "observability", "title": "Logging, metrics, tracing",
     "kinds": [],
     "topics": ["Logging", "Observability"]},
    {"slug": "ci-config", "title": "CI workflows and configuration files",
     "kinds": ["workflow-linting", "file-hygiene"],
     "topics": ["CI/CD", "Configurations"]},
    {"slug": "dependencies", "title": "Dependencies and lockfiles",
     "kinds": ["dependency-audit", "lockfile-check", "version-matrix"],
     "topics": []},
    {"slug": "tests", "title": "The tests themselves",
     "kinds": ["mutation-testing", "version-matrix"],
     "topics": ["Testing"]},
    {"slug": "docs", "title": "Documentation and comments",
     "kinds": ["docs-build", "spelling"],
     "topics": ["Documentation"]},
]
CHANGE_SLUGS = [change["slug"] for change in CHANGES]
PROMPTS_PER_CHANGE_PAGE = 5
PROMPTS_PER_CHANGE_RAW = 12
COMMANDS_PER_TOOL = 3
EXAMPLE_REPOS = 6
LANGUAGE_SHARE = 0.2


def method_page_slug(method: str) -> str:
    return METHOD_GUIDE[method]["slug"]


def _scan_index(scans: dict[str, dict]) -> dict[str, dict]:
    """Scans keyed by lowercase repository, the key every guide join uses."""
    return {repo.lower(): scan for repo, scan in scans.items()}


def repository_languages(entries: list[dict]) -> dict[str, set[str]]:
    """Lowercase repository -> playbook languages it counts towards.

    A repository counts towards a language when at least a fifth of its
    instructions are written in it, or when it is the repository's most common
    instruction language.
    """
    by_entry_language = {name: lang["slug"] for lang in LANGUAGES for name in lang["entry_languages"]}
    counts: dict[str, Counter[str]] = defaultdict(Counter)
    for entry in entries:
        if entry["repository"] and entry["language"] in by_entry_language:
            counts[entry["repository"].lower()][by_entry_language[entry["language"]]] += 1
    totals = Counter(entry["repository"].lower() for entry in entries if entry["repository"])
    result: dict[str, set[str]] = {}
    for repo, counter in counts.items():
        top = counter.most_common(1)[0][0]
        result[repo] = {lang for lang, n in counter.items() if n >= LANGUAGE_SHARE * totals[repo]} | {top}
    return result


def tool_catalog(scans: dict[str, dict]) -> dict[str, dict]:
    """Tool id -> profile merged with what the scans report about it."""
    catalog: dict[str, dict] = {}
    for scan in scans.values():
        for check in scan["verifications"]:
            tool = check["tool"]
            if not tool or tool in catalog:
                continue
            profile = TOOL_PROFILES.get(tool)
            if profile is None:
                print(f"note: tool {tool!r} has no TOOL_PROFILES entry and is left out of the guide")
                continue
            catalog[tool] = {
                "id": tool,
                "method": check["method"],
                "kind": profile["kind"],
                "languages": profile["languages"],
                "upstream": check["upstream"],
                "docs": check["docs"],
                "autofix": check["autofix"],
                "exit_codes": check["exit_codes"],
            }
    return catalog


def _indirect(command: str) -> bool:
    """A command recorded as the hook or action that runs a tool, not something to type."""
    return command.startswith(("pre-commit hook ", "uses ")) or command.endswith(" via environment")


def _via(command: str) -> str:
    """How an indirect command runs the tool, in words."""
    if command.startswith("uses "):
        return f"GitHub Action {command.removeprefix('uses ')}"
    if command.startswith("pre-commit hook "):
        return f"pre-commit hook {command.removeprefix('pre-commit hook ')}"
    return command


def _applies(tool: dict, language: str) -> bool:
    return ANY_LANGUAGE in tool["languages"] or language in tool["languages"]


def _tool_usage(tool_id: str, repos: list[str], index: dict[str, dict]) -> tuple[list[str], Counter[str], Counter[str]]:
    """Repositories that run the tool, the commands they run and where."""
    users: list[str] = []
    commands: Counter[str] = Counter()
    triggers: Counter[str] = Counter()
    for repo in repos:
        checks = [c for c in index[repo]["verifications"] if c["tool"] == tool_id]
        if not checks:
            continue
        users.append(repo)
        for check in checks:
            commands.update({" ".join(command.split()) for command in check["commands"]})
            triggers.update(check["triggers"])
    return users, commands, triggers


def _repo_name(repo: str, index: dict[str, dict]) -> dict:
    scan = index[repo]
    return {"repository": scan["repository"], "slug": scan["slug"]}


def build_tool_rows(catalog: dict[str, dict], repos: list[str], index: dict[str, dict], stars: dict[str, int],
                    language: str | None) -> list[dict]:
    rows = []
    for tool in catalog.values():
        if language and not _applies(tool, language):
            continue
        users, commands, triggers = _tool_usage(tool["id"], repos, index)
        if not users:
            continue
        users.sort(key=lambda repo: stars.get(repo, 0), reverse=True)
        runnable = [command for command, _ in commands.most_common() if not _indirect(command)]
        indirect = [command for command, _ in commands.most_common() if _indirect(command)]
        rows.append(
            {
                **tool,
                "repos": len(users),
                "share": round(100 * len(users) / len(repos)) if repos else 0,
                "commands": [
                    command
                    for command, _ in sorted(commands.items(), key=lambda item: (_indirect(item[0]), -item[1], item[0]))
                ][:COMMANDS_PER_TOOL],
                "run": runnable[0] if runnable else None,
                "via": _via(indirect[0]) if indirect else None,
                "triggers": [trigger for trigger in VERIFICATION_TRIGGERS if triggers[trigger]],
                "examples": [_repo_name(repo, index) for repo in users[:EXAMPLE_REPOS]],
            }
        )
    rows.sort(key=lambda row: (-row["repos"], row["id"]))
    return rows


COMPILER_NOTE = "The compiler type-checks on every build and test run; a failing build is this check failing."


def _kind_rows(tools: list[dict], kinds: list[str], compiled: bool = False) -> list[dict]:
    titles = {k["slug"]: k for k in CHECK_KINDS}
    rows = []
    for kind in kinds:
        options = [tool for tool in tools if tool["kind"] == kind]
        rows.append(
            {
                "kind": kind,
                "title": titles[kind]["title"],
                "method": titles[kind]["method"],
                "method_slug": method_page_slug(titles[kind]["method"]),
                "catches": titles[kind]["catches"],
                "tool": options[0] if options else None,
                "alternatives": [{"id": t["id"], "repos": t["repos"], "share": t["share"]} for t in options[1:4]],
                "note": COMPILER_NOTE if compiled and kind == "type-checking" and not options else None,
            }
        )
    return rows


def _prompt_rows(entries: list[dict], topics: list[str], limit: int) -> tuple[list[dict], int]:
    matching = [e for e in entries if e["topic"] in topics]
    matching.sort(key=lambda e: (e["comments"], e["updated"]), reverse=True)
    return [entry_row(e) for e in matching[:limit]], len(matching)


def build_playbooks(entries: list[dict], scans: dict[str, dict]) -> list[dict]:
    index = _scan_index(scans)
    catalog = tool_catalog(scans)
    languages_of = repository_languages(entries)
    stars: dict[str, int] = {}
    for entry in entries:
        repo = entry["repository"].lower()
        stars[repo] = max(stars.get(repo, 0), entry["stars"])

    playbooks = []
    for language in LANGUAGES:
        slug = language["slug"]
        lang_entries = [e for e in entries if e["language"] in language["entry_languages"]]
        if not lang_entries:
            continue
        repos = sorted(repo for repo, langs in languages_of.items() if slug in langs and repo in index)
        tools = build_tool_rows(catalog, repos, index, stars, slug)
        changes = []
        for change in CHANGES:
            prompts, total = _prompt_rows(lang_entries, change["topics"], PROMPTS_PER_CHANGE_RAW)
            changes.append(
                {
                    "slug": change["slug"],
                    "title": change["title"],
                    "topics": change["topics"],
                    "checks": _kind_rows(tools, change["kinds"], language.get("compiled", False)),
                    "prompts": prompts,
                    "prompts_shown": prompts[:PROMPTS_PER_CHANGE_PAGE],
                    "prompt_count": total,
                }
            )
        repos.sort(key=lambda repo: stars.get(repo, 0), reverse=True)
        playbooks.append(
            {
                "slug": slug,
                "title": language["title"],
                "extensions": language["extensions"],
                "entry_languages": language["entry_languages"],
                "prompts": len(lang_entries),
                "repos": len(repos),
                "sample": [
                    {**_repo_name(repo, index), "checks": sum(1 for c in index[repo]["verifications"] if c["tool"])}
                    for repo in repos
                ],
                "tools": tools,
                "baseline": changes[0],
                "changes": changes[1:],
                "headline": [row["tool"]["id"] for row in changes[0]["checks"] if row["tool"]],
                "raw_md": f"{SITE_URL}/raw/verify/{slug}.md",
                "raw_json": f"{SITE_URL}/raw/verify/{slug}.json",
                "url": f"{SITE_URL}/verify/{slug}/",
            }
        )
    return playbooks


def build_methods(entries: list[dict], scans: dict[str, dict]) -> list[dict]:
    index = _scan_index(scans)
    catalog = tool_catalog(scans)
    stars: dict[str, int] = {}
    for entry in entries:
        repo = entry["repository"].lower()
        stars[repo] = max(stars.get(repo, 0), entry["stars"])
    repos = sorted(index)
    tools = build_tool_rows(catalog, repos, index, stars, None)
    using = {
        method: {repo for repo in repos if any(c["method"] == method and c["tool"] for c in index[repo]["verifications"])}
        for method in GUIDE_METHODS
    }
    titles = {m["slug"]: m["title"] for m in VERIFICATION_METHODS}
    methods = []
    for method in GUIDE_METHODS:
        kinds = []
        for kind in (k for k in CHECK_KINDS if k["method"] == method):
            kind_tools = [tool for tool in tools if tool["kind"] == kind["slug"]]
            kinds.append(
                {
                    **kind,
                    "tools": kind_tools,
                    "changes": [{"slug": c["slug"], "title": c["title"]} for c in CHANGES if kind["slug"] in c["kinds"]],
                }
            )
        methods.append(
            {
                "method": method,
                "slug": method_page_slug(method),
                "title": titles[method],
                **{key: METHOD_GUIDE[method][key] for key in ("summary", "when")},
                "repos": len(using[method]),
                "share": round(100 * len(using[method]) / len(repos)) if repos else 0,
                "kinds": kinds,
                "tools": len([tool for tool in tools if tool["method"] == method]),
            }
        )
    return methods


# --------------------------------------------------------------------------- #
# Verification catalog: a matrix of tactics (columns) and techniques (cells),
# modelled on MITRE ATT&CK. `_catalog/techniques.json` is the editorial layer;
# techniques that name check kinds get their procedure examples, tools and
# configuration signals counted from the scans.
# --------------------------------------------------------------------------- #

CATALOG_DIR = Path("_catalog")
TECHNIQUE_ID = re.compile(r"V\d{4}")
TACTIC_ID = re.compile(r"VA\d{2}")
PROCEDURE_EXAMPLES = 40
SIGNALS_PER_TECHNIQUE = 6


def read_catalog(directory: Path = CATALOG_DIR) -> dict:
    """Tactics, techniques and packages, validated against the tables above. Fails the build when inconsistent."""
    packages = json.loads((directory / "packages.json").read_text(encoding="utf-8"))
    raw = json.loads((directory / "techniques.json").read_text(encoding="utf-8"))
    tactics, techniques = raw["tactics"], raw["techniques"]
    problems: list[str] = []
    tactic_ids = [t["id"] for t in tactics]
    for tactic in tactics:
        if not TACTIC_ID.fullmatch(tactic["id"]):
            problems.append(f"tactic {tactic['id']!r}: id must look like VA01")
        if tactic.get("method"):
            if tactic["method"] not in METHOD_GUIDE or tactic["slug"] != method_page_slug(tactic["method"]):
                problems.append(f"tactic {tactic['id']}: method and slug must match METHOD_GUIDE")
        elif not all(tactic.get(key) for key in ("title", "summary", "when")):
            problems.append(f"tactic {tactic['id']}: needs title, summary and when")
    covered = [method for t in tactics if (method := t.get("method"))]
    if sorted(covered) != sorted(GUIDE_METHODS):
        problems.append("every verification method needs exactly one tactic")
    seen: set[str] = set()
    kinds: list[str] = []
    for technique in techniques:
        where = f"technique {technique.get('id')!r}"
        ids = [technique["id"], *(sub["id"] for sub in technique["subtechniques"])]
        if not TECHNIQUE_ID.fullmatch(technique["id"]):
            problems.append(f"{where}: id must look like V1001")
        if any(not sub["id"].startswith(technique["id"] + ".") for sub in technique["subtechniques"]):
            problems.append(f"{where}: sub-technique ids must extend the technique id")
        if seen & set(ids):
            problems.append(f"{where}: duplicate id")
        seen.update(ids)
        if technique["tactic"] not in tactic_ids:
            problems.append(f"{where}: unknown tactic {technique['tactic']!r}")
        if missing := [p for p in technique["packages"] if p not in packages]:
            problems.append(f"{where}: unknown packages {missing}")
        if not technique["craft"] or not technique["reverse"] or not technique["packages"]:
            problems.append(f"{where}: needs craft steps, reverse-engineering signals and packages")
        for kind in technique["kinds"]:
            if kind not in CHECK_KIND_SLUGS:
                problems.append(f"{where}: unknown check kind {kind!r}")
            elif (tactic := next(t for t in tactics if t["id"] == technique["tactic"])).get("method") != next(
                k["method"] for k in CHECK_KINDS if k["slug"] == kind
            ):
                problems.append(f"{where}: check kind {kind!r} belongs to another method than tactic {tactic['id']}")
        kinds.extend(technique["kinds"])
    if sorted(kinds) != sorted(CHECK_KIND_SLUGS):
        problems.append("every check kind must belong to exactly one technique")
    if problems:
        raise SystemExit("invalid catalog in _catalog/:\n  " + "\n  ".join(problems))
    return {"tactics": tactics, "techniques": techniques, "packages": packages}


def evidence_signal(path: str) -> str:
    """Where a check is configured, generalised so it can be looked for in any repository."""
    if path.startswith(".github/workflows/"):
        return ".github/workflows/*.yml"
    if "/.husky/" in f"/{path}":
        return ".husky/" + path.rsplit("/", 1)[-1]
    return path.rsplit("/", 1)[-1]


def _runs(check: dict) -> bool:
    return bool(check["tool"]) and not check["declared_only"] and check["tool"] in TOOL_PROFILES


def kinds_run(scan: dict) -> set[str]:
    """Check kinds a scanned repository runs: recognised tools only, declared-only entries excluded."""
    return {TOOL_PROFILES[c["tool"]]["kind"] for c in scan["verifications"] if _runs(c)}


def build_catalog(entries: list[dict], scans: dict[str, dict], catalog_source: dict) -> dict:
    index = _scan_index(scans)
    catalog = tool_catalog(scans)
    stars: dict[str, int] = {}
    for entry in entries:
        repo = entry["repository"].lower()
        stars[repo] = max(stars.get(repo, 0), entry["stars"])
    repos = sorted(index, key=lambda repo: (-stars.get(repo, 0), repo))
    tools = build_tool_rows(catalog, repos, index, stars, None)
    packages = catalog_source["packages"]
    kind_titles = {k["slug"]: k for k in CHECK_KINDS}
    method_titles = {m["slug"]: m["title"] for m in VERIFICATION_METHODS}

    techniques = []
    for source in catalog_source["techniques"]:
        kinds = set(source["kinds"])
        procedures = []
        signals: dict[str, set[str]] = defaultdict(set)
        for repo in repos:
            checks = [c for c in index[repo]["verifications"] if _runs(c) and TOOL_PROFILES[c["tool"]]["kind"] in kinds]
            if not checks:
                continue
            for check in checks:
                for evidence in check["evidence"]:
                    signals[evidence_signal(evidence["path"])].add(repo)
            first = checks[0]["evidence"][0] if checks[0]["evidence"] else None
            procedures.append(
                {
                    **_repo_name(repo, index),
                    "tools": sorted({c["tool"] for c in checks}),
                    "triggers": [t for t in VERIFICATION_TRIGGERS if any(t in c["triggers"] for c in checks)],
                    "evidence": f"{first['path']} {first['locator']}".strip() if first else None,
                }
            )
        techniques.append(
            {
                "id": source["id"],
                "name": source["name"],
                "tactic": source["tactic"],
                "description": source["description"],
                "subtechniques": source["subtechniques"],
                "kinds": [
                    {"slug": kind, "title": kind_titles[kind]["title"], "catches": kind_titles[kind]["catches"]}
                    for kind in source["kinds"]
                ],
                "detected": bool(source["kinds"]),
                "packages": [{"id": p, **packages[p]} for p in source["packages"]],
                "tools": [
                    {key: tool[key] for key in ("id", "repos", "share", "run", "via", "triggers", "docs", "upstream", "autofix")}
                    for tool in tools
                    if tool["kind"] in kinds
                ],
                "craft": source["craft"],
                "reverse": source["reverse"],
                "signals": [
                    {"signal": signal, "repos": len(users)}
                    for signal, users in sorted(signals.items(), key=lambda item: (-len(item[1]), item[0]))[:SIGNALS_PER_TECHNIQUE]
                ],
                "repos": len(procedures),
                "share": round(100 * len(procedures) / len(repos)) if repos and source["kinds"] else None,
                "procedures": procedures[:PROCEDURE_EXAMPLES],
                "url": f"{SITE_URL}/techniques/{source['id']}/",
            }
        )

    tactics = []
    for source in catalog_source["tactics"]:
        method = source.get("method")
        guide = METHOD_GUIDE[method] if method else source
        members = [t for t in techniques if t["tactic"] == source["id"]]
        for technique in members:
            technique["tactic_slug"] = source["slug"]
            technique["tactic_title"] = method_titles[method] if method else source["title"]
        tactics.append(
            {
                "id": source["id"],
                "slug": source["slug"],
                "method": method,
                "short": source["short"],
                "title": method_titles[method] if method else source["title"],
                "summary": guide["summary"],
                "when": guide["when"],
                "detected": bool(method),
                "techniques": members,
                "subtechniques": sum(len(t["subtechniques"]) for t in members),
                "url": f"{SITE_URL}/methods/{source['slug']}/",
            }
        )
    return {
        "tactics": tactics,
        "techniques": len(techniques),
        "subtechniques": sum(t["subtechniques"] for t in tactics),
        "packages": len({p["id"] for t in techniques for p in t["packages"]}),
        "scanned": len(repos),
        "kind_technique": {kind["slug"]: t["id"] for t in techniques for kind in t["kinds"]},
    }


def build_catalog_markdown(catalog: dict) -> str:
    """The whole catalog as one markdown file for agents."""
    lines = [
        "# Verification catalog",
        "",
        f"{len(catalog['tactics'])} tactics, {catalog['techniques']} techniques, {catalog['subtechniques']} "
        f"sub-techniques. Usage counts are from {catalog['scanned']} scanned source repositories. "
        f"Leaderboard: {SITE_URL}/raw/leaderboard.json",
        "",
    ]
    for tactic in catalog["tactics"]:
        lines += [f"## {tactic['id']} {tactic['title']}", "", tactic["summary"], "", f"When: {tactic['when']}", ""]
        for t in tactic["techniques"]:
            usage = f" Run by {t['repos']} of {catalog['scanned']} scanned repositories." if t["detected"] else ""
            lines += [f"### {t['id']} {t['name']}", "", t["description"] + usage, ""]
            if t["subtechniques"]:
                lines += ["Sub-techniques:", ""]
                lines += [f"- {s['id']} {s['name']}: {s['description']}" for s in t["subtechniques"]]
                lines.append("")
            lines += ["Craft it:", ""]
            lines += [f"{n}. {step}" for n, step in enumerate(t["craft"], 1)]
            lines += ["", "Reverse engineer it (look for):", ""]
            lines += [f"- {signal}" for signal in t["reverse"]]
            lines += [f"- `{s['signal']}` (configures it in {s['repos']} scanned repositories)" for s in t["signals"]]
            lines += ["", "Open-source packages: " + ", ".join(f"[{p['name']}]({p['url']})" for p in t["packages"])]
            if t["tools"]:
                lines.append("Tools seen in scans: " + ", ".join(f"`{tool['id']}` ({tool['repos']})" for tool in t["tools"]))
            lines.append("")
    return "\n".join(lines)


# --------------------------------------------------------------------------- #
# Leaderboard, adapted from VerifyBench (Yan et al., arXiv:2505.15801).
#
# VerifyBench scores a verifier by accuracy on labelled items, reported per
# answer type with an unweighted average across the types, plus a Hard split
# of items strong models disagree on. Here an item is a (repository, check
# kind) pair where the kind applies to the repository's languages; it counts
# as correct when the repository runs a recognised tool of that kind. The
# answer types become the five verification methods, and the Hard split is
# the kinds fewer than HARD_ADOPTION of the repositories they apply to run.
# --------------------------------------------------------------------------- #

PAPER_URL = "https://arxiv.org/abs/2505.15801"
HARD_ADOPTION = 0.25


def applicable_kinds(languages: set[str], scan: dict) -> set[str]:
    """Check kinds that apply to a repository: a recognised tool exists for one of its languages, or for any language.

    Workflow linting applies wherever the scan found a GitHub Actions workflow, whatever the language.
    """
    kinds = {
        profile["kind"]
        for profile in TOOL_PROFILES.values()
        if ANY_LANGUAGE in profile["languages"] or languages & set(profile["languages"])
    }
    if any(e["path"].startswith(".github/workflows/") for c in scan["verifications"] for e in c["evidence"]):
        kinds.add("workflow-linting")
    return kinds


def build_leaderboard(entries: list[dict], scans: dict[str, dict], tactics: list[dict] | None = None) -> dict:
    """`tactics` orders the method columns and names them; defaults to the scanner's method order."""
    order = [t["method"] for t in tactics or [] if t.get("method")] or GUIDE_METHODS
    shorts = {t["method"]: t["short"] for t in tactics or [] if t.get("method")}
    index = _scan_index(scans)
    languages_of = repository_languages(entries)
    stars: dict[str, int] = {}
    for entry in entries:
        repo = entry["repository"].lower()
        stars[repo] = max(stars.get(repo, 0), entry["stars"])
    method_of = {k["slug"]: k["method"] for k in CHECK_KINDS}

    items: dict[str, tuple[set[str], set[str]]] = {}
    for repo, scan in index.items():
        run = kinds_run(scan)
        items[repo] = (applicable_kinds(languages_of.get(repo, set()), scan) | run, run)

    adoption = {}
    for kind in CHECK_KIND_SLUGS:
        # Share among repositories the kind applies to by language or workflow, so running it elsewhere does not inflate it.
        applies = [
            repo for repo in items if kind in applicable_kinds(languages_of.get(repo, set()), index[repo])
        ]
        adoption[kind] = sum(kind in items[repo][1] for repo in applies) / len(applies) if applies else 0.0
    hard = {kind for kind, share in adoption.items() if share < HARD_ADOPTION}

    def accuracy(applicable: set[str], run: set[str]) -> float | None:
        return round(100 * len(applicable & run) / len(applicable), 1) if applicable else None

    rows = []
    for repo, (applicable, run) in items.items():
        by_method = {
            method: accuracy({k for k in applicable if method_of[k] == method}, run) for method in order
        }
        scored = [score for score in by_method.values() if score is not None]
        rows.append(
            {
                **_repo_name(repo, index),
                "stars": stars.get(repo, 0),
                "methods": by_method,
                "avg": round(sum(scored) / len(scored), 1) if scored else 0.0,
                "hard": accuracy(applicable & hard, run),
                "items": len(applicable),
                "correct": len(applicable & run),
                "kinds": sorted(run),
                "languages": sorted(languages_of.get(repo, set())),
            }
        )
    rows.sort(key=lambda r: (-r["avg"], -(r["hard"] or 0), -r["correct"], r["repository"].lower()))
    previous = None
    for position, row in enumerate(rows, 1):
        key = (row["avg"], row["hard"], row["correct"])
        row["rank"] = previous[1] if previous and previous[0] == key else position
        previous = (key, row["rank"])
    titles = {m["slug"]: m["title"] for m in VERIFICATION_METHODS}
    return {
        "paper": {"title": "VerifyBench: Benchmarking Reference-based Reward Systems for Large Language Models", "url": PAPER_URL},
        "methods": [
            {"method": m, "slug": method_page_slug(m), "title": titles[m], "short": shorts.get(m, titles[m])} for m in order
        ],
        "hard_threshold": round(100 * HARD_ADOPTION),
        "hard_kinds": [
            {"slug": k["slug"], "title": k["title"], "adoption": round(100 * adoption[k["slug"]])}
            for k in CHECK_KINDS
            if k["slug"] in hard
        ],
        "kinds": [{"slug": k, "adoption": round(100 * adoption[k])} for k in CHECK_KIND_SLUGS],
        "count": len(rows),
        "rows": rows,
    }


def build_source_pages(entries: list[dict], scans: dict[str, dict]) -> dict[str, dict]:
    """One page per source repository, keyed by its slug: checks and prompts."""
    index = _scan_index(scans)
    catalog = tool_catalog(scans)
    grouped: dict[str, list[dict]] = defaultdict(list)
    for entry in entries:
        if entry["repository"]:
            grouped[repository_slug(entry["repository"])].append(entry)
    titles = {m["slug"]: m["title"] for m in VERIFICATION_METHODS}
    kind_titles = {k["slug"]: k["title"] for k in CHECK_KINDS}
    pages = {}
    for slug, group in grouped.items():
        names = Counter(e["repository"] for e in group)
        scan = index.get(group[0]["repository"].lower())
        repository = scan["repository"] if scan else names.most_common(1)[0][0]
        methods = []
        other: list[str] = []
        if scan:
            for method in GUIDE_METHODS:
                checks = [
                    {
                        "tool": c["tool"],
                        "kind": kind_titles.get(catalog.get(c["tool"], {}).get("kind", ""), ""),
                        "commands": c["commands"][:COMMANDS_PER_TOOL],
                        "triggers": c["triggers"],
                        "evidence": list(dict.fromkeys(e["path"] for e in c["evidence"]))[:4],
                        "docs": c["docs"] or c["upstream"],
                        "declared_only": c["declared_only"],
                    }
                    for c in scan["verifications"]
                    if c["method"] == method and c["tool"]
                ]
                if checks:
                    methods.append({"method": method, "slug": method_page_slug(method), "title": titles[method], "checks": checks})
            other = [c["commands"][0] for c in scan["verifications"] if not c["tool"] and c["commands"]][:40]
        group.sort(key=lambda e: (e["comments"], e["updated"]), reverse=True)
        pages[slug] = {
            "slug": slug,
            "repository": repository,
            "ref": scan["ref"] if scan else None,
            "stars": max(e["stars"] for e in group),
            "domain": Counter(e["domain"] for e in group).most_common(1)[0][0],
            "updated": max((e["updated"] for e in group), default=""),
            "tools": sorted({c["tool"] for m in methods for c in m["checks"]}),
            "methods": methods,
            "other": other,
            "other_count": sum(1 for c in scan["verifications"] if not c["tool"]) if scan else 0,
            "entries": [entry_row(e) for e in group],
        }
    return pages


def build_domain_checks(entries: list[dict], scans: dict[str, dict], limit: int = 8) -> dict[str, list[dict]]:
    """Domain slug -> the tools most of its scanned repositories run."""
    index = _scan_index(scans)
    repos_by_domain: dict[str, set[str]] = defaultdict(set)
    for entry in entries:
        if entry["repository"].lower() in index:
            repos_by_domain[entry["domain"]].add(entry["repository"].lower())
    result = {}
    for domain, repos in repos_by_domain.items():
        counts = Counter(tool for repo in repos for tool in {c["tool"] for c in index[repo]["verifications"] if c["tool"]})
        result[domain] = [
            {"tool": tool, "repos": n, "share": round(100 * n / len(repos))} for tool, n in counts.most_common(limit)
        ]
    return result


def language_for_entry(entry: dict) -> str | None:
    for language in LANGUAGES:
        if entry["language"] in language["entry_languages"]:
            return language["slug"]
    return None


def _md_exit_codes(codes: dict[str, str]) -> str:
    return "; ".join(f"`{code}` {meaning}" for code, meaning in codes.items())


def build_playbook_markdown(playbook: dict) -> str:
    """The playbook an agent loads before it verifies a change in this language."""
    lines = [
        f"# Verifying {playbook['title']} changes",
        "",
        f"Files: {', '.join(f'`{ext}`' for ext in playbook['extensions'])}. "
        f"Derived from {playbook['repos']} scanned source repositories and {playbook['prompts']} review prompts "
        f"on {SITE_URL}. Page: {playbook['url']}",
        "",
        "How to use this: run every check under *Run on every change*. Then, for each section under *Add when "
        "the change touches* that describes your diff, run its checks too. Checks catch what a tool can find; "
        "then apply the listed review prompts for what tools miss (fetch each prompt's raw URL).",
        "",
        "Usage is the share of scanned repositories in this language that run the tool. A missing tool means no "
        "scanned repository runs one the scanner recognises: fall back to the prompts.",
        "",
    ]

    def check_lines(rows: list[dict]) -> list[str]:
        out = []
        for row in rows:
            tool = row["tool"]
            if not tool:
                detail = row["note"] or f"no tool detected in the sample. Catches: {row['catches']}"
                out.append(f"- **{row['title']}** — {detail}")
                continue
            if tool["run"]:
                command = f" Command seen: `{tool['run']}`."
            elif tool["via"]:
                command = f" Runs via {tool['via']}."
            else:
                command = ""
            fix = " Autofixes." if tool["autofix"] else ""
            codes = f" Exit codes: {_md_exit_codes(tool['exit_codes'])}." if tool["exit_codes"] else ""
            docs = f" Docs: {tool['docs'] or tool['upstream']}" if (tool["docs"] or tool["upstream"]) else ""
            alternatives = ", ".join(f"{a['id']} ({a['share']}%)" for a in row["alternatives"])
            alt = f" Alternatives: {alternatives}." if alternatives else ""
            out.append(
                f"- **{row['title']}**: `{tool['id']}` ({tool['share']}% of repos).{command}{fix}{codes}{alt}{docs}"
            )
        return out

    def prompt_lines(change: dict) -> list[str]:
        if not change["prompts"]:
            return []
        out = ["", f"Review prompts ({change['prompt_count']} in total, most discussed first):", ""]
        out += [
            f"- [{p['title']}]({SITE_URL}/raw/{p['slug']}.md) — {p['repository']}, {p['topic']}"
            for p in change["prompts"]
        ]
        return out

    baseline = playbook["baseline"]
    lines += ["## Run on every change", "", *check_lines(baseline["checks"]), *prompt_lines(baseline), ""]
    lines += ["## Add when the change touches", ""]
    for change in playbook["changes"]:
        if not change["checks"] and not change["prompts"]:
            continue
        lines += [f"### {change['title']}", ""]
        lines += check_lines(change["checks"]) or ["- No tool-based check applies; rely on the prompts."]
        lines += [*prompt_lines(change), ""]
    if playbook["sample"]:
        lines += [
            "## Source repositories",
            "",
            ", ".join(f"[{r['repository']}]({SITE_URL}/sources/{r['slug']}/)" for r in playbook["sample"]),
            "",
        ]
    return "\n".join(lines)


def strip_playbook(playbook: dict) -> dict:
    """The JSON form of a playbook: no page-only fields."""
    def change(c: dict) -> dict:
        return {key: value for key, value in c.items() if key != "prompts_shown"} | {
            "prompts": [{**p, "raw": f"{SITE_URL}/raw/{p['slug']}.md"} for p in c["prompts"]]
        }

    return {
        **{key: value for key, value in playbook.items() if key not in ("baseline", "changes")},
        "baseline": change(playbook["baseline"]),
        "changes": [change(c) for c in playbook["changes"]],
    }


# --------------------------------------------------------------------------- #
# Writers
# --------------------------------------------------------------------------- #


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, separators=(",", ":"))
        handle.write("\n")
    print(f"  wrote {path} ({path.stat().st_size / 1024:.0f} KB)")


def shorten(text: str, limit: int) -> str:
    if len(text) <= limit:
        return text
    return text[:limit].rsplit(" ", 1)[0] + "…"


def top_values(values: list[str], limit: int) -> list[str]:
    return [value for value, _ in Counter(v for v in values if v).most_common(limit)]


def build_domains(entries: list[dict]) -> list[dict]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for entry in entries:
        grouped[entry["domain"]].append(entry)

    domains = []
    for definition in DOMAINS:
        group = grouped.get(definition["slug"], [])
        if not group:
            continue
        domains.append(
            {
                **definition,
                "count": len(group),
                "repositories": len({e["repository"] for e in group if e["repository"]}),
                "updated": max((e["updated"] for e in group), default=""),
                "topics": top_values([e["topic"] for e in group], 8),
                "languages": top_values([e["language"] for e in group], 8),
            }
        )
    return domains


def build_sources(entries: list[dict], verifications: dict[str, dict] | None = None) -> list[dict]:
    verifications = verifications or {}
    grouped: dict[str, list[dict]] = defaultdict(list)
    for entry in entries:
        if entry["repository"]:
            grouped[entry["repository"]].append(entry)

    sources = [
        {
            "repository": repo,
            "count": len(group),
            "stars": max(e["stars"] for e in group),
            "domain": Counter(e["domain"] for e in group).most_common(1)[0][0],
            "updated": max((e["updated"] for e in group), default=""),
            "reviewers": len({author for e in group for author in e["authors"]}),
            "checks": len(verifications[repo]["verifications"]) if repo in verifications else None,
            "checks_url": f"/raw/verifications/{verifications[repo]['slug']}.json" if repo in verifications else None,
            "page": repository_slug(repo),
        }
        for repo, group in grouped.items()
    ]
    sources.sort(key=lambda s: (s["updated"], s["count"]), reverse=True)
    return sources


def build_people(entries: list[dict], limit: int = 60) -> list[dict]:
    """Reviewers whose feedback the corpus is derived from, most-cited first."""
    counts: Counter[str] = Counter()
    repos: dict[str, set[str]] = defaultdict(set)
    last: dict[str, str] = {}
    for entry in entries:
        for author in entry["authors"]:
            counts[author] += 1
            repos[author].add(entry["repository"])
            if entry["updated"] > last.get(author, ""):
                last[author] = entry["updated"]

    return [
        {
            "name": name,
            "count": count,
            "repositories": len(repos[name]),
            "updated": last.get(name, ""),
        }
        for name, count in counts.most_common(limit)
    ]


def entry_row(entry: dict) -> dict:
    return {
        "slug": entry["slug"],
        "title": entry["title"],
        "description": entry["description"],
        "repository": entry["repository"],
        "domain": entry["domain"],
        "topic": entry["topic"],
        "language": entry["language"],
        "updated": entry["updated"],
        "comments": entry["comments"],
        "stars": entry["stars"],
    }


def build_site_overview(entries: list[dict], domains: list[dict], playbooks: list[dict] | None = None) -> str:
    """The homepage as markdown: what this is, where everything is, one screen.

    `llms.txt` lists all 5k instructions, which is the wrong thing to hand an
    agent that has just landed on the site. This is the short version, and it is
    what the homepage advertises as its markdown representation.
    """
    lines = [
        "# Awesome Reviewers",
        "",
        "Which checks to run on the code you are writing, and the review prompts for what those",
        "checks miss. Checks come from the CI workflows, pre-commit hooks and task runners of",
        "production open-source repositories; prompts are distilled from their code review",
        "discussions. Map a changed file to a language, load that language's playbook, run its",
        f"checks, then apply its prompts. Start at {SITE_URL}/raw/verify/index.json.",
        "",
        f"{len(entries)} instructions from "
        f"{len({e['repository'] for e in entries if e['repository']})} repositories, "
        f"across {len(domains)} domains. Last updated "
        f"{max((e['updated'] for e in entries), default='')}.",
        "",
        "## Developer resources",
        "",
    ]
    for resource in DEV_RESOURCES:
        lines.append(
            f"- [{resource['name']}]({SITE_URL}{resource['path']}) "
            f"({resource['media_type']}) — {resource['description']}"
        )

    if playbooks:
        lines += ["", "## Verification playbooks", "", "| Language | Baseline checks | Playbook |", "| --- | --- | --- |"]
        for playbook in playbooks:
            lines.append(
                f"| {playbook['title']} | {', '.join(playbook['headline']) or '-'} | "
                f"[{playbook['slug']}.md]({playbook['raw_md']}) |"
            )

    lines += [
        "",
        "## Domains",
        "",
        "| Domain | Instructions | Updated | Bundle |",
        "| --- | --- | --- | --- |",
    ]
    for domain in domains:
        lines.append(
            f"| {domain['title']} | {domain['count']} | {domain['updated']} | "
            f"[{domain['slug']}.md]({SITE_URL}/raw/bundles/{domain['slug']}.md) |"
        )

    lines += [
        "",
        "## Errors",
        "",
        f"RFC 9457 problem details, documented at {ERRORS_DOCS_URL}#errors.",
        "",
    ]
    for problem in build_problems():
        lines.append(f"- `{problem['code']}` ({problem['status']}) — {problem['resolution']}")

    lines += ["", "Apache-2.0. Source: https://github.com/baz-scm/awesome-reviewers", ""]
    return "\n".join(lines)


def write_raw(entries: list[dict], domains: list[dict], playbooks: list[dict] | None = None) -> None:
    if RAW_DIR.exists():
        shutil.rmtree(RAW_DIR)
    (RAW_DIR / "bundles").mkdir(parents=True)

    if any(entry["slug"] == SITE_OVERVIEW_SLUG for entry in entries):
        raise SystemExit(
            f"an instruction is slugged '{SITE_OVERVIEW_SLUG}', which collides with "
            f"{RAW_DIR}/{SITE_OVERVIEW_SLUG}.md; rename the instruction"
        )
    (RAW_DIR / f"{SITE_OVERVIEW_SLUG}.md").write_text(
        build_site_overview(entries, domains, playbooks), encoding="utf-8"
    )

    titles = {d["slug"]: d["title"] for d in DOMAINS}
    bundles: dict[str, list[str]] = defaultdict(list)

    for entry in entries:
        # The header is an HTML comment rather than YAML front matter on purpose:
        # front matter would make Jekyll render these as pages instead of serving
        # them verbatim. It still parses as YAML once the comment markers are cut.
        header = "\n".join(
            [
                "<!--",
                f"title: {entry['title']}",
                f"domain: {entry['domain']}",
                f"topic: {entry['topic']}",
                f"language: {entry['language']}",
                f"source: {entry['repository']}",
                f"updated: {entry['updated']}",
                f"url: {SITE_URL}/reviewers/{entry['slug']}/",
                "-->",
                "",
                "",
            ]
        )
        (RAW_DIR / f"{entry['slug']}.md").write_text(
            f"{header}{entry['body']}\n", encoding="utf-8"
        )
        bundles[entry["domain"]].append(
            f"## {entry['title']}\n\n"
            f"<!-- source: {entry['repository']} | topic: {entry['topic']} | "
            f"language: {entry['language']} | updated: {entry['updated']} -->\n\n"
            f"{entry['body']}\n"
        )

    for domain in domains:
        slug = domain["slug"]
        body = "\n---\n\n".join(bundles[slug])
        (RAW_DIR / "bundles" / f"{slug}.md").write_text(
            f"# {titles[slug]}\n\n"
            f"{domain['blurb']}\n\n"
            f"{domain['count']} instructions from {domain['repositories']} repositories. "
            f"Last updated {domain['updated']}.\n\n"
            f"---\n\n{body}",
            encoding="utf-8",
        )

    write_json(
        RAW_DIR / "index.json",
        {
            "generated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "count": len(entries),
            "site": SITE_URL,
            "domains": [
                {
                    "slug": d["slug"],
                    "title": d["title"],
                    "count": d["count"],
                    "updated": d["updated"],
                    "bundle": f"{SITE_URL}/raw/bundles/{d['slug']}.md",
                }
                for d in domains
            ],
            "entries": [
                {**entry_row(e), "raw": f"{SITE_URL}/raw/{e['slug']}.md"} for e in entries
            ],
        },
    )
    print(f"  wrote {len(entries)} raw endpoints and {len(domains)} bundles")


def write_verifications(scans: dict[str, dict]) -> None:
    """`/raw/verifications/<repository>.json` per scan, plus an index of all of them."""
    directory = RAW_DIR / "verifications"
    directory.mkdir(parents=True, exist_ok=True)
    for scan in scans.values():
        (directory / f"{scan['slug']}.json").write_text(
            json.dumps(
                {
                    "repository": scan["repository"],
                    "ref": scan["ref"],
                    "methods": VERIFICATION_METHODS,
                    "verifications": scan["verifications"],
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
    summaries = sorted((verification_summary(scan) for scan in scans.values()), key=lambda s: s["repository"])
    write_json(
        directory / "index.json",
        {
            "generated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "count": len(summaries),
            "methods": VERIFICATION_METHODS,
            "repositories": summaries,
        },
    )
    print(f"  wrote {len(scans)} verification scans")


def write_catalog(catalog: dict, leaderboard: dict) -> None:
    """Data for /methods/, /techniques/<id>/ and /leaderboard/, plus /raw/catalog.* and /raw/leaderboard.json."""
    write_json(DATA_DIR / "catalog.json", catalog)
    write_json(DATA_DIR / "leaderboard.json", leaderboard)
    generated = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    write_json(RAW_DIR / "catalog.json", {"generated": generated, **catalog})
    (RAW_DIR / "catalog.md").write_text(build_catalog_markdown(catalog), encoding="utf-8")
    write_json(RAW_DIR / "leaderboard.json", {"generated": generated, **leaderboard})
    directory = Path("techniques")
    directory.mkdir(exist_ok=True)
    for stale in directory.glob("*.html"):
        stale.unlink()
    for tactic in catalog["tactics"]:
        for t in tactic["techniques"]:
            (directory / f"{t['id']}.html").write_text(
                "---\n"
                "layout: technique\n"
                f"technique: {t['id']}\n"
                f"title: {json.dumps(t['id'] + ' ' + t['name'])}\n"
                f"permalink: /techniques/{t['id']}/\n"
                f"description: {json.dumps(t['description'])}\n"
                "---\n",
                encoding="utf-8",
            )
    print(f"  wrote catalog: {len(catalog['tactics'])} tactics, {catalog['techniques']} techniques; "
          f"leaderboard: {leaderboard['count']} repositories")


def write_guide(playbooks: list[dict], methods: list[dict], source_pages: dict[str, dict],
                tactics: list[dict] | None = None) -> None:
    """Data and stub pages for /verify/, /methods/ and /sources/<repository>/, plus /raw/verify/."""
    extensions = {ext: p["slug"] for p in playbooks for ext in p["extensions"]}
    write_json(
        DATA_DIR / "verify.json",
        {
            "languages": playbooks,
            "methods": methods,
            "kinds": CHECK_KINDS,
            "changes": [{"slug": c["slug"], "title": c["title"], "kinds": c["kinds"], "topics": c["topics"]} for c in CHANGES],
            "extensions": extensions,
            "scanned": len({page["repository"].lower() for page in source_pages.values() if page["ref"]}),
        },
    )
    write_json(DATA_DIR / "source_pages.json", source_pages)

    directory = RAW_DIR / "verify"
    directory.mkdir(parents=True, exist_ok=True)
    for playbook in playbooks:
        (directory / f"{playbook['slug']}.md").write_text(build_playbook_markdown(playbook), encoding="utf-8")
        write_json(directory / f"{playbook['slug']}.json", strip_playbook(playbook))
    write_json(
        directory / "index.json",
        {
            "generated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "how_to_use": (
                "Map each changed file to a language with `extensions`, fetch that language's playbook, run "
                "the baseline checks, add the checks for every change kind the diff touches, then apply the "
                "listed review prompts."
            ),
            "extensions": extensions,
            "languages": [
                {
                    "slug": p["slug"],
                    "title": p["title"],
                    "extensions": p["extensions"],
                    "repos": p["repos"],
                    "prompts": p["prompts"],
                    "baseline": p["headline"],
                    "markdown": p["raw_md"],
                    "json": p["raw_json"],
                }
                for p in playbooks
            ],
            "changes": [{"slug": c["slug"], "title": c["title"], "kinds": c["kinds"], "topics": c["topics"]} for c in CHANGES],
            "kinds": CHECK_KINDS,
            "methods": [
                {key: m[key] for key in ("method", "slug", "title", "summary", "when", "repos", "share")} for m in methods
            ],
        },
    )

    stubs = {
        Path("verify"): [
            ("language", "verify", p["slug"], f"Verifying {p['title']} changes",
             f"Which checks to run on {p['title']} code, from the source repositories that run them, "
             "and the review prompts for what those checks miss.")
            for p in playbooks
        ],
        Path("methods"): [
            ("method", "method", t["slug"], f"{t['id']} {t['title']}", t["summary"]) for t in tactics or []
        ],
        Path("sources"): [
            ("source", "source", page["slug"], page["repository"],
             f"The checks {page['repository']} runs and the review prompts derived from it.")
            for page in source_pages.values()
        ],
    }
    for directory_path, pages in stubs.items():
        directory_path.mkdir(exist_ok=True)
        for stale in directory_path.glob("*.html"):
            stale.unlink()
        for layout, key, slug, title, description in pages:
            (directory_path / f"{slug}.html").write_text(
                "---\n"
                f"layout: {layout}\n"
                f"{key}: {slug}\n"
                f"title: {json.dumps(title)}\n"
                f"permalink: /{directory_path.name}/{slug}/\n"
                f"description: {json.dumps(description)}\n"
                "---\n",
                encoding="utf-8",
            )
    print(f"  wrote {len(playbooks)} playbooks, {len(tactics or [])} method pages, {len(source_pages)} source pages")


def write_search(entries: list[dict]) -> None:
    """Compact column-oriented index, fetched on the first keystroke.

    Descriptions are truncated rather than dropped: most of the vocabulary people
    search for ("tool calling", "kv cache") lives in the description, not the
    title, and the tail of a description rarely adds a new term. Repeated values
    (domain, topic, language, repository) are interned to keep the file small.
    """
    domains = DOMAIN_SLUGS
    topics = sorted({e["topic"] for e in entries})
    languages = sorted({e["language"] for e in entries})
    repositories = sorted({e["repository"] for e in entries})

    write_json(
        SEARCH_PATH,
        {
            "fields": ["slug", "title", "domain", "topic", "language", "repository", "updated", "comments", "description"],
            "domains": domains,
            "topics": topics,
            "languages": languages,
            "repositories": repositories,
            "entries": [
                [
                    e["slug"],
                    e["title"],
                    domains.index(e["domain"]),
                    topics.index(e["topic"]),
                    languages.index(e["language"]),
                    repositories.index(e["repository"]),
                    e["updated"],
                    e["comments"],
                    shorten(e["description"], 130),
                ]
                for e in entries
            ],
        },
    )


def write_domain_pages(domains: list[dict]) -> None:
    """One thin stub per domain; `_layouts/domain.html` does the rendering."""
    pages_dir = Path("domains")
    pages_dir.mkdir(exist_ok=True)
    for stale in pages_dir.glob("*.html"):
        stale.unlink()
    for domain in domains:
        (pages_dir / f"{domain['slug']}.html").write_text(
            "---\n"
            "layout: domain\n"
            f"domain: {domain['slug']}\n"
            f"title: {domain['title']}\n"
            f"permalink: /domains/{domain['slug']}/\n"
            f"description: {domain['blurb']}\n"
            "---\n",
            encoding="utf-8",
        )
    print(f"  wrote {len(domains)} domain pages")


# --------------------------------------------------------------------------- #
# Machine interface: developer resources, error format, OpenAPI description
# --------------------------------------------------------------------------- #

# One entry per machine-readable file the site publishes. This list is the
# single source of truth for openapi.json, llms.txt, the site overview and robots.txt, so an
# endpoint cannot be added in one place and forgotten in the others.
DEV_RESOURCES: list[dict] = [
    {
        "name": "OpenAPI description",
        "path": "/openapi.json",
        "media_type": "application/vnd.oai.openapi+json;version=3.1",
        "description": "OpenAPI 3.1 description of every endpoint listed here.",
    },
    {
        "name": "Site overview",
        "path": "/raw/site.md",
        "media_type": "text/markdown",
        "description": "The homepage as markdown: what this is, the endpoints, the domains.",
    },
    {
        "name": "Verification playbooks index",
        "path": "/raw/verify/index.json",
        "media_type": "application/json",
        "description": (
            "Start here to verify a change: file extension -> language, the playbook URL per language, "
            "the change kinds, check kinds and verification methods."
        ),
    },
    {
        "name": "Verification playbook",
        "path": "/raw/verify/<language>.md",
        "media_type": "text/markdown",
        "description": (
            "Which checks to run on code in one language: the tool most source repositories run per check kind, "
            "the command, exit codes, autofix, then the review prompts per kind of change."
        ),
    },
    {
        "name": "Verification playbook (JSON)",
        "path": "/raw/verify/<language>.json",
        "media_type": "application/json",
        "description": "The same playbook as structured data, with every candidate tool and its usage share.",
    },
    {
        "name": "Verification catalog",
        "path": "/raw/catalog.md",
        "media_type": "text/markdown",
        "description": (
            "Every verification tactic and technique with sub-techniques, open-source packages, steps to build it "
            "and signals that a codebase already runs it."
        ),
    },
    {
        "name": "Verification catalog (JSON)",
        "path": "/raw/catalog.json",
        "media_type": "application/json",
        "description": "The same catalog as structured data, with procedure examples and tool usage counted from the scans.",
    },
    {
        "name": "Verification leaderboard",
        "path": "/raw/leaderboard.json",
        "media_type": "application/json",
        "description": (
            "Every scanned source repository ranked by catalog coverage: accuracy per verification method, "
            "their average and a hard split, adapted from VerifyBench."
        ),
    },
    {
        "name": "Corpus index",
        "path": "/raw/index.json",
        "media_type": "application/json",
        "description": "Every instruction: slug, title, description, domain, topic, language, source, updated, raw URL.",
    },
    {
        "name": "Single instruction",
        "path": "/raw/<slug>.md",
        "media_type": "text/markdown",
        "description": "One instruction as plain markdown, with a commented header carrying its metadata.",
    },
    {
        "name": "Domain bundle",
        "path": "/raw/bundles/<domain>.md",
        "media_type": "text/markdown",
        "description": "Every instruction in one domain, concatenated into a single markdown file.",
    },
    {
        "name": "Verifications index",
        "path": "/raw/verifications/index.json",
        "media_type": "application/json",
        "description": "Every scanned source repository: commit, check count per verification method, tools, scan URL.",
    },
    {
        "name": "Repository verifications",
        "path": "/raw/verifications/<repository>.json",
        "media_type": "application/json",
        "description": (
            "The checks one source repository runs: tool, method, commands, where it runs, "
            "evidence, upstream, documented exit codes."
        ),
    },
    {
        "name": "Source discussions",
        "path": "/<slug>.json",
        "media_type": "application/json",
        "description": "The review discussions one instruction was derived from.",
    },
    {
        "name": "Search index",
        "path": "/assets/data/search.json",
        "media_type": "application/json",
        "description": "Column-oriented index used by the search box: smaller, truncated descriptions.",
    },
    {
        "name": "LLM index",
        "path": "/llms.txt",
        "media_type": "text/plain",
        "description": "Domain-grouped listing of the whole corpus with raw URLs.",
    },
    {
        "name": "Sitemap",
        "path": "/sitemap.xml",
        "media_type": "application/xml",
        "description": "Every HTML page on the site.",
    },
]

# Error responses follow RFC 9457 (problem details for HTTP APIs). `code` and
# `resolution` are extension members: the code is stable for matching, the
# resolution says what to do next without reading prose.
PROBLEM_TYPES: list[dict] = [
    {
        "code": "not_found",
        "status": 404,
        "title": "Resource not found",
        "detail": "Nothing is published at this path.",
        "resolution": (
            f"Every published path is listed in {SITE_URL}/raw/index.json and "
            f"{SITE_URL}/llms.txt. Look the slug up there and retry."
        ),
    },
    {
        "code": "not_acceptable",
        "status": 406,
        "title": "No acceptable representation",
        "detail": "The Accept header rules out every representation of this resource.",
        "resolution": (
            "Send Accept: text/markdown for markdown, text/html for the rendered page, "
            "application/json for the JSON endpoints, or */* to take whatever is served."
        ),
    },
]


def problem_type_url(code: str) -> str:
    """The URI an RFC 9457 `type` member points at, resolvable to its docs."""
    return f"{ERRORS_DOCS_URL}#error-{code.replace('_', '-')}"


def build_problems() -> list[dict]:
    return [{**problem, "type": problem_type_url(problem["code"])} for problem in PROBLEM_TYPES]


def build_openapi(entries: list[dict], domains: list[dict], version: str) -> dict:
    """OpenAPI 3.1 description of the static endpoints the site publishes.

    Everything here is a plain file served over HTTP: no key, no rate limit and
    no method other than GET. The description exists so an agent can discover
    the shape of the corpus without scraping the HTML.
    """
    example_slug = entries[0]["slug"] if entries else "example-instruction"
    domain_slugs = [d["slug"] for d in domains]
    present = {language_for_entry(e) for e in entries}
    language_slugs = [slug for slug in LANGUAGE_SLUGS if slug in present]
    language_parameter = {
        "name": "language",
        "in": "path",
        "required": True,
        "description": "Playbook language slug. `/raw/verify/index.json` maps file extensions to it.",
        "schema": {"type": "string", "enum": language_slugs},
        "example": language_slugs[0] if language_slugs else "python",
    }
    problems = build_problems()

    def error_response(status: int) -> dict:
        problem = next(p for p in problems if p["status"] == status)
        return {
            "description": problem["title"],
            "content": {
                "application/problem+json": {
                    "schema": {"$ref": "#/components/schemas/Problem"},
                    "example": {
                        "type": problem["type"],
                        "title": problem["title"],
                        "status": problem["status"],
                        "detail": problem["detail"],
                        "code": problem["code"],
                        "resolution": problem["resolution"],
                    },
                },
                "text/html": {
                    "schema": {
                        "type": "string",
                        "description": (
                            "Served to clients that accept HTML. The page carries the same "
                            'problem details in a script element with id "problem", plus a '
                            "markdown recovery block."
                        ),
                    }
                },
            },
        }

    def markdown_response(description: str) -> dict:
        return {
            "description": description,
            "content": {"text/markdown": {"schema": {"type": "string"}}},
        }

    return {
        "openapi": "3.1.0",
        "info": {
            "title": "Awesome Reviewers API",
            "version": version,
            "summary": "Read-only endpoints for the Awesome Reviewers instruction corpus.",
            "description": (
                "Awesome Reviewers publishes expert engineering instructions for AI and "
                "infrastructure domains, distilled from code review discussions in production "
                "open-source repositories.\n\n"
                "Every endpoint is a static file served over HTTPS. There is no key, no rate "
                "limit and no method other than GET. Responses are immutable for a given build; "
                "the `updated` field on each entry carries the date of the most recent review "
                "comment behind it, so a scheduled job can diff against its last run instead of "
                "refetching the corpus.\n\n"
                "Errors follow RFC 9457 problem details."
            ),
            "contact": {
                "name": "Awesome Reviewers",
                "url": "https://github.com/baz-scm/awesome-reviewers",
            },
            "license": {
                "name": "Apache-2.0",
                "identifier": "Apache-2.0",
            },
        },
        "externalDocs": {
            "description": "Awesome Reviewers README",
            "url": f"{REPOSITORY_URL}#readme",
        },
        "servers": [{"url": SITE_URL, "description": "Production"}],
        "tags": [
            {"name": "instructions", "description": "Single instructions and domain bundles."},
            {"name": "indexes", "description": "Machine-readable indexes of the whole corpus."},
            {"name": "discovery", "description": "Descriptions of the site itself."},
            {
                "name": "verifications",
                "description": "The checks each source repository runs: linters, type checkers, tests, proofs.",
            },
            {
                "name": "playbooks",
                "description": "Which checks to run on code in a given language, and the prompts for what they miss.",
            },
            {
                "name": "catalog",
                "description": "Verification tactics and techniques, and the leaderboard of source repositories.",
            },
        ],
        "paths": {
            "/raw/index.json": {
                "get": {
                    "operationId": "getIndex",
                    "summary": "Machine-readable index of the whole corpus",
                    "description": (
                        "One row per instruction plus one row per domain. The `raw` field on each "
                        "entry is the URL of that instruction as markdown."
                    ),
                    "tags": ["indexes"],
                    "responses": {
                        "200": {
                            "description": "The corpus index",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/Index"}
                                }
                            },
                        },
                        "404": error_response(404),
                    },
                }
            },
            "/raw/site.md": {
                "get": {
                    "operationId": "getSiteOverview",
                    "summary": "The homepage as markdown",
                    "description": (
                        "What the corpus is, the endpoints, and one row per domain with its "
                        "instruction count and bundle URL. The short alternative to /llms.txt."
                    ),
                    "tags": ["discovery"],
                    "responses": {
                        "200": markdown_response("The site overview"),
                        "406": error_response(406),
                    },
                }
            },
            "/raw/{slug}.md": {
                "get": {
                    "operationId": "getInstruction",
                    "summary": "One instruction as markdown",
                    "description": (
                        "The instruction body, preceded by an HTML comment carrying its title, "
                        "domain, topic, language, source repository, last-updated date and the "
                        "URL of its page. Slugs come from `/raw/index.json`."
                    ),
                    "tags": ["instructions"],
                    "parameters": [{"$ref": "#/components/parameters/Slug"}],
                    "responses": {
                        "200": markdown_response("The instruction"),
                        "404": error_response(404),
                        "406": error_response(406),
                    },
                }
            },
            "/raw/bundles/{domain}.md": {
                "get": {
                    "operationId": "getDomainBundle",
                    "summary": "Every instruction in one domain, concatenated",
                    "description": (
                        "One markdown file per domain: a heading, the domain blurb, its counts and "
                        "then every instruction in it, each with a source comment."
                    ),
                    "tags": ["instructions"],
                    "parameters": [
                        {
                            "name": "domain",
                            "in": "path",
                            "required": True,
                            "description": "Domain slug.",
                            "schema": {"type": "string", "enum": domain_slugs},
                            "example": domain_slugs[0] if domain_slugs else "ai-agents",
                        }
                    ],
                    "responses": {
                        "200": markdown_response("The domain bundle"),
                        "404": error_response(404),
                        "406": error_response(406),
                    },
                }
            },
            "/raw/verify/index.json": {
                "get": {
                    "operationId": "getPlaybooksIndex",
                    "summary": "Entry point for verifying a change",
                    "description": (
                        "File extension -> language, one row per language with its playbook URLs and "
                        "baseline tools, the change kinds with the check kinds each one calls for, the "
                        "check kinds and the verification methods."
                    ),
                    "tags": ["playbooks", "indexes"],
                    "responses": {
                        "200": {
                            "description": "The playbooks index",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/PlaybooksIndex"}
                                }
                            },
                        },
                        "404": error_response(404),
                    },
                }
            },
            "/raw/verify/{language}.md": {
                "get": {
                    "operationId": "getPlaybook",
                    "summary": "The verification playbook for one language, as markdown",
                    "description": (
                        "Checks to run on every change, then checks and review prompts per kind of change. "
                        "Each check names the tool most scanned repositories in this language run, its "
                        "share, a command seen in those repositories, its exit codes and whether it autofixes."
                    ),
                    "tags": ["playbooks"],
                    "parameters": [language_parameter],
                    "responses": {
                        "200": markdown_response("The playbook"),
                        "404": error_response(404),
                        "406": error_response(406),
                    },
                }
            },
            "/raw/verify/{language}.json": {
                "get": {
                    "operationId": "getPlaybookData",
                    "summary": "The verification playbook for one language, as JSON",
                    "description": "The playbook with every candidate tool, its share and example repositories.",
                    "tags": ["playbooks"],
                    "parameters": [language_parameter],
                    "responses": {
                        "200": {
                            "description": "The playbook",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/Playbook"}
                                }
                            },
                        },
                        "404": error_response(404),
                    },
                }
            },
            "/raw/verifications/index.json": {
                "get": {
                    "operationId": "getVerificationsIndex",
                    "summary": "Every scanned source repository and its verification counts",
                    "description": (
                        "One row per source repository that has a verification scan: the commit it "
                        "was scanned at, the number of checks per method, the tools found and the "
                        "URL of the full scan."
                    ),
                    "tags": ["verifications", "indexes"],
                    "responses": {
                        "200": {
                            "description": "The verifications index",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/VerificationsIndex"}
                                }
                            },
                        },
                        "404": error_response(404),
                    },
                }
            },
            "/raw/verifications/{repository}.json": {
                "get": {
                    "operationId": "getRepositoryVerifications",
                    "summary": "The checks one source repository runs",
                    "description": (
                        "Every verification found in the repository's CI workflows, pre-commit hooks, "
                        "task runners and manifests: the tool, its method, the commands that run it, "
                        "where it runs, the files it was found in, its upstream project and its "
                        "documented exit codes."
                    ),
                    "tags": ["verifications"],
                    "parameters": [
                        {
                            "name": "repository",
                            "in": "path",
                            "required": True,
                            "description": (
                                "Source repository as owner-name, lowercase, other characters replaced "
                                "by '-'. Listed in /raw/verifications/index.json."
                            ),
                            "schema": {"type": "string", "pattern": "^[a-z0-9.-]+$"},
                            "example": "pallets-flask",
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "The repository's verifications",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/RepositoryVerifications"}
                                }
                            },
                        },
                        "404": error_response(404),
                    },
                }
            },
            "/{slug}.json": {
                "get": {
                    "operationId": "getDiscussions",
                    "summary": "The review discussions one instruction was derived from",
                    "description": (
                        "Provenance for a single instruction: the review threads it was distilled "
                        "from, each with its comments, authors and timestamps."
                    ),
                    "tags": ["instructions"],
                    "parameters": [{"$ref": "#/components/parameters/Slug"}],
                    "responses": {
                        "200": {
                            "description": "The source discussions",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "array",
                                        "items": {"$ref": "#/components/schemas/Discussion"},
                                    }
                                }
                            },
                        },
                        "404": error_response(404),
                    },
                }
            },
            "/assets/data/search.json": {
                "get": {
                    "operationId": "getSearchIndex",
                    "summary": "Compact column-oriented search index",
                    "description": (
                        "The index the search box fetches. Repeated values (domain, topic, "
                        "language, repository) are interned: each entry holds their positions in "
                        "the sibling arrays. Descriptions are truncated. Prefer `/raw/index.json` "
                        "unless size matters."
                    ),
                    "tags": ["indexes"],
                    "responses": {
                        "200": {
                            "description": "The search index",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/SearchIndex"}
                                }
                            },
                        },
                        "404": error_response(404),
                    },
                }
            },
            "/llms.txt": {
                "get": {
                    "operationId": "getLlmsTxt",
                    "summary": "Domain-grouped index of the corpus for LLM consumers",
                    "tags": ["indexes"],
                    "responses": {
                        "200": {
                            "description": "The llms.txt index",
                            "content": {"text/plain": {"schema": {"type": "string"}}},
                        },
                        "404": error_response(404),
                    },
                }
            },
            "/raw/catalog.md": {
                "get": {
                    "operationId": "getCatalogMarkdown",
                    "summary": "The verification catalog as markdown",
                    "description": (
                        "Tactics in order, each technique with its sub-techniques, the steps to build it, the "
                        "signals that show a codebase runs it, and open-source packages that implement it."
                    ),
                    "tags": ["catalog"],
                    "responses": {
                        "200": {
                            "description": "The catalog",
                            "content": {"text/markdown": {"schema": {"type": "string"}}},
                        },
                        "404": error_response(404),
                    },
                }
            },
            "/raw/catalog.json": {
                "get": {
                    "operationId": "getCatalog",
                    "summary": "The verification catalog as structured data",
                    "description": (
                        "Tactics with their techniques. Techniques the scanner can detect carry usage counts, "
                        "the tools seen, configuration signals and procedure examples from the scans."
                    ),
                    "tags": ["catalog"],
                    "responses": {
                        "200": {
                            "description": "The catalog",
                            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Catalog"}}},
                        },
                        "404": error_response(404),
                    },
                }
            },
            "/raw/leaderboard.json": {
                "get": {
                    "operationId": "getLeaderboard",
                    "summary": "Source repositories ranked by verification coverage",
                    "description": (
                        "One row per scanned repository: accuracy per verification method over the check kinds "
                        "that apply to it, the unweighted average, the hard split and the rank."
                    ),
                    "tags": ["catalog"],
                    "responses": {
                        "200": {
                            "description": "The leaderboard",
                            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Leaderboard"}}},
                        },
                        "404": error_response(404),
                    },
                }
            },
            "/openapi.json": {
                "get": {
                    "operationId": "getOpenapi",
                    "summary": "This description",
                    "tags": ["discovery"],
                    "responses": {
                        "200": {
                            "description": "The OpenAPI description",
                            "content": {
                                "application/vnd.oai.openapi+json;version=3.1": {
                                    "schema": {"type": "object"}
                                }
                            },
                        }
                    },
                }
            },
            "/sitemap.xml": {
                "get": {
                    "operationId": "getSitemap",
                    "summary": "Every HTML page on the site",
                    "tags": ["discovery"],
                    "responses": {
                        "200": {
                            "description": "The sitemap",
                            "content": {"application/xml": {"schema": {"type": "string"}}},
                        }
                    },
                }
            },
        },
        "components": {
            "parameters": {
                "Slug": {
                    "name": "slug",
                    "in": "path",
                    "required": True,
                    "description": "Instruction slug, as published in /raw/index.json.",
                    "schema": {"type": "string", "pattern": "^[a-z0-9-]+$"},
                    "example": example_slug,
                }
            },
            "schemas": {
                "Entry": {
                    "type": "object",
                    "description": "One instruction.",
                    "required": ["slug", "title", "domain", "raw"],
                    "properties": {
                        "slug": {"type": "string", "example": example_slug},
                        "title": {"type": "string"},
                        "description": {"type": "string"},
                        "repository": {
                            "type": "string",
                            "description": "Source repository, as owner/name.",
                        },
                        "domain": {"type": "string", "enum": domain_slugs},
                        "topic": {"type": "string"},
                        "language": {"type": "string"},
                        "updated": {
                            "type": "string",
                            "format": "date",
                            "description": "Date of the most recent review comment behind it.",
                        },
                        "comments": {"type": "integer", "minimum": 0},
                        "stars": {
                            "type": "integer",
                            "minimum": 0,
                            "description": "Stars on the source repository when it was imported.",
                        },
                        "raw": {
                            "type": "string",
                            "format": "uri",
                            "description": "URL of this instruction as markdown.",
                        },
                    },
                },
                "Domain": {
                    "type": "object",
                    "description": "One domain, with its bundle URL.",
                    "required": ["slug", "title", "count", "bundle"],
                    "properties": {
                        "slug": {"type": "string", "enum": domain_slugs},
                        "title": {"type": "string"},
                        "count": {"type": "integer", "minimum": 0},
                        "updated": {"type": "string", "format": "date"},
                        "bundle": {"type": "string", "format": "uri"},
                    },
                },
                "Index": {
                    "type": "object",
                    "required": ["generated", "count", "site", "domains", "entries"],
                    "properties": {
                        "generated": {
                            "type": "string",
                            "format": "date-time",
                            "description": "When this index was built.",
                        },
                        "count": {"type": "integer", "minimum": 0},
                        "site": {"type": "string", "format": "uri"},
                        "domains": {
                            "type": "array",
                            "items": {"$ref": "#/components/schemas/Domain"},
                        },
                        "entries": {
                            "type": "array",
                            "items": {"$ref": "#/components/schemas/Entry"},
                        },
                    },
                },
                "SearchIndex": {
                    "type": "object",
                    "required": ["fields", "entries"],
                    "properties": {
                        "fields": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Column names, in the order each entry row holds them.",
                        },
                        "domains": {"type": "array", "items": {"type": "string"}},
                        "topics": {"type": "array", "items": {"type": "string"}},
                        "languages": {"type": "array", "items": {"type": "string"}},
                        "repositories": {"type": "array", "items": {"type": "string"}},
                        "entries": {
                            "type": "array",
                            "description": (
                                "One row per instruction. Domain, topic, language and repository "
                                "are indexes into the arrays above."
                            ),
                            "items": {"type": "array"},
                        },
                    },
                },
                "VerificationMethod": {
                    "type": "object",
                    "required": ["slug", "title"],
                    "properties": {
                        "slug": {"type": "string", "enum": VERIFICATION_METHOD_SLUGS},
                        "title": {"type": "string"},
                    },
                },
                "Verification": {
                    "type": "object",
                    "description": "One check a repository runs, merged across every place it is invoked.",
                    "required": ["tool", "method", "commands", "triggers", "evidence"],
                    "properties": {
                        "tool": {
                            "type": ["string", "null"],
                            "description": "Catalog id of the tool; null when the command is unclassified.",
                        },
                        "method": {"type": "string", "enum": VERIFICATION_METHOD_SLUGS},
                        "commands": {"type": "array", "items": {"type": "string"}},
                        "triggers": {
                            "type": "array",
                            "items": {"type": "string", "enum": VERIFICATION_TRIGGERS},
                            "description": "Where it runs: pre-commit hooks, CI, or local task runners.",
                        },
                        "evidence": {
                            "type": "array",
                            "description": "Files and locations the check was found in, in the order followed.",
                            "items": {
                                "type": "object",
                                "required": ["path", "locator"],
                                "properties": {
                                    "path": {"type": "string"},
                                    "locator": {"type": "string"},
                                },
                            },
                        },
                        "upstream": {"type": ["string", "null"], "format": "uri"},
                        "docs": {"type": ["string", "null"], "format": "uri"},
                        "exit_codes": {
                            "type": "object",
                            "description": "Documented exit codes, keyed by code.",
                            "additionalProperties": {"type": "string"},
                        },
                        "autofix": {"type": "boolean", "description": "The tool can rewrite files to fix findings."},
                        "declared_only": {
                            "type": "boolean",
                            "description": "Configured or installed, but nothing found that runs it.",
                        },
                    },
                },
                "RepositoryVerifications": {
                    "type": "object",
                    "required": ["repository", "ref", "methods", "verifications"],
                    "properties": {
                        "repository": {"type": "string", "description": "owner/name"},
                        "ref": {"type": "string", "description": "Commit sha the scan read."},
                        "methods": {
                            "type": "array",
                            "items": {"$ref": "#/components/schemas/VerificationMethod"},
                        },
                        "verifications": {
                            "type": "array",
                            "items": {"$ref": "#/components/schemas/Verification"},
                        },
                    },
                },
                "PlaybooksIndex": {
                    "type": "object",
                    "required": ["generated", "extensions", "languages", "changes", "kinds", "methods"],
                    "properties": {
                        "generated": {"type": "string", "format": "date-time"},
                        "how_to_use": {"type": "string"},
                        "extensions": {
                            "type": "object",
                            "description": "File extension (or file name, e.g. Dockerfile) -> language slug.",
                            "additionalProperties": {"type": "string", "enum": language_slugs},
                        },
                        "languages": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "required": ["slug", "title", "extensions", "markdown", "json"],
                                "properties": {
                                    "slug": {"type": "string", "enum": language_slugs},
                                    "title": {"type": "string"},
                                    "extensions": {"type": "array", "items": {"type": "string"}},
                                    "repos": {"type": "integer", "minimum": 0},
                                    "prompts": {"type": "integer", "minimum": 0},
                                    "baseline": {
                                        "type": "array",
                                        "description": "Tools recommended for every change.",
                                        "items": {"type": "string"},
                                    },
                                    "markdown": {"type": "string", "format": "uri"},
                                    "json": {"type": "string", "format": "uri"},
                                },
                            },
                        },
                        "changes": {"type": "array", "items": {"$ref": "#/components/schemas/ChangeKind"}},
                        "kinds": {"type": "array", "items": {"$ref": "#/components/schemas/CheckKind"}},
                        "methods": {"type": "array", "items": {"type": "object"}},
                    },
                },
                "ChangeKind": {
                    "type": "object",
                    "description": "What a change touches, the check kinds it calls for and the prompt topics that cover it.",
                    "required": ["slug", "title", "kinds", "topics"],
                    "properties": {
                        "slug": {"type": "string", "enum": CHANGE_SLUGS},
                        "title": {"type": "string"},
                        "kinds": {"type": "array", "items": {"type": "string", "enum": CHECK_KIND_SLUGS}},
                        "topics": {"type": "array", "items": {"type": "string"}},
                    },
                },
                "CheckKind": {
                    "type": "object",
                    "required": ["slug", "title", "method", "catches"],
                    "properties": {
                        "slug": {"type": "string", "enum": CHECK_KIND_SLUGS},
                        "title": {"type": "string"},
                        "method": {"type": "string", "enum": VERIFICATION_METHOD_SLUGS},
                        "catches": {"type": "string"},
                    },
                },
                "Tool": {
                    "type": "object",
                    "required": ["id", "method", "kind", "repos", "share"],
                    "properties": {
                        "id": {"type": "string"},
                        "method": {"type": "string", "enum": VERIFICATION_METHOD_SLUGS},
                        "kind": {"type": "string", "enum": CHECK_KIND_SLUGS},
                        "languages": {"type": "array", "items": {"type": "string"}},
                        "repos": {"type": "integer", "minimum": 0, "description": "Scanned repositories that run it."},
                        "share": {
                            "type": "integer",
                            "minimum": 0,
                            "maximum": 100,
                            "description": "Percent of the scanned repositories in scope that run it.",
                        },
                        "commands": {"type": "array", "items": {"type": "string"}},
                        "triggers": {"type": "array", "items": {"type": "string", "enum": VERIFICATION_TRIGGERS}},
                        "autofix": {"type": "boolean"},
                        "exit_codes": {"type": "object", "additionalProperties": {"type": "string"}},
                        "docs": {"type": ["string", "null"], "format": "uri"},
                        "upstream": {"type": ["string", "null"], "format": "uri"},
                    },
                },
                "Playbook": {
                    "type": "object",
                    "required": ["slug", "title", "extensions", "tools", "baseline", "changes"],
                    "properties": {
                        "slug": {"type": "string", "enum": language_slugs},
                        "title": {"type": "string"},
                        "extensions": {"type": "array", "items": {"type": "string"}},
                        "repos": {"type": "integer", "minimum": 0},
                        "prompts": {"type": "integer", "minimum": 0},
                        "tools": {"type": "array", "items": {"$ref": "#/components/schemas/Tool"}},
                        "baseline": {"$ref": "#/components/schemas/PlaybookSection"},
                        "changes": {"type": "array", "items": {"$ref": "#/components/schemas/PlaybookSection"}},
                    },
                },
                "PlaybookSection": {
                    "type": "object",
                    "required": ["slug", "title", "checks", "prompts"],
                    "properties": {
                        "slug": {"type": "string", "enum": CHANGE_SLUGS},
                        "title": {"type": "string"},
                        "topics": {"type": "array", "items": {"type": "string"}},
                        "checks": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "required": ["kind", "title", "tool"],
                                "properties": {
                                    "kind": {"type": "string", "enum": CHECK_KIND_SLUGS},
                                    "title": {"type": "string"},
                                    "catches": {"type": "string"},
                                    "tool": {
                                        "description": "The most-run tool for this check, or null when none was detected.",
                                        "oneOf": [{"$ref": "#/components/schemas/Tool"}, {"type": "null"}],
                                    },
                                },
                            },
                        },
                        "prompts": {"type": "array", "items": {"$ref": "#/components/schemas/Entry"}},
                        "prompt_count": {"type": "integer", "minimum": 0},
                    },
                },
                "Catalog": {
                    "type": "object",
                    "required": ["generated", "tactics", "techniques", "subtechniques", "scanned"],
                    "properties": {
                        "generated": {"type": "string", "format": "date-time"},
                        "techniques": {"type": "integer", "minimum": 0},
                        "subtechniques": {"type": "integer", "minimum": 0},
                        "packages": {"type": "integer", "minimum": 0},
                        "scanned": {"type": "integer", "minimum": 0},
                        "tactics": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "required": ["id", "slug", "title", "summary", "when", "techniques"],
                                "properties": {
                                    "id": {"type": "string", "pattern": "^VA[0-9]{2}$"},
                                    "slug": {"type": "string"},
                                    "title": {"type": "string"},
                                    "summary": {"type": "string"},
                                    "when": {"type": "string"},
                                    "method": {"type": ["string", "null"]},
                                    "detected": {"type": "boolean"},
                                    "techniques": {
                                        "type": "array",
                                        "items": {
                                            "type": "object",
                                            "required": ["id", "name", "description", "subtechniques", "packages", "craft", "reverse"],
                                            "properties": {
                                                "id": {"type": "string", "pattern": "^V[0-9]{4}$"},
                                                "name": {"type": "string"},
                                                "description": {"type": "string"},
                                                "subtechniques": {"type": "array", "items": {"type": "object"}},
                                                "packages": {"type": "array", "items": {"type": "object"}},
                                                "craft": {"type": "array", "items": {"type": "string"}},
                                                "reverse": {"type": "array", "items": {"type": "string"}},
                                                "repos": {"type": "integer", "minimum": 0},
                                                "share": {"type": ["integer", "null"]},
                                                "procedures": {"type": "array", "items": {"type": "object"}},
                                            },
                                        },
                                    },
                                },
                            },
                        },
                    },
                },
                "Leaderboard": {
                    "type": "object",
                    "required": ["generated", "paper", "methods", "count", "rows"],
                    "properties": {
                        "generated": {"type": "string", "format": "date-time"},
                        "paper": {"type": "object"},
                        "methods": {"type": "array", "items": {"type": "object"}},
                        "hard_threshold": {"type": "integer"},
                        "hard_kinds": {"type": "array", "items": {"type": "object"}},
                        "count": {"type": "integer", "minimum": 0},
                        "rows": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "required": ["rank", "repository", "slug", "methods", "avg", "hard", "items", "correct"],
                                "properties": {
                                    "rank": {"type": "integer", "minimum": 1},
                                    "repository": {"type": "string"},
                                    "slug": {"type": "string"},
                                    "methods": {
                                        "type": "object",
                                        "description": "Accuracy (0-100) per method slug; null when no check kind of it applies.",
                                        "additionalProperties": {"type": ["number", "null"]},
                                    },
                                    "avg": {"type": "number"},
                                    "hard": {"type": ["number", "null"]},
                                    "items": {"type": "integer", "minimum": 0},
                                    "correct": {"type": "integer", "minimum": 0},
                                },
                            },
                        },
                    },
                },
                "VerificationsIndex": {
                    "type": "object",
                    "required": ["generated", "count", "methods", "repositories"],
                    "properties": {
                        "generated": {"type": "string", "format": "date-time"},
                        "count": {"type": "integer", "minimum": 0},
                        "methods": {
                            "type": "array",
                            "items": {"$ref": "#/components/schemas/VerificationMethod"},
                        },
                        "repositories": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "required": ["repository", "ref", "count", "methods", "url"],
                                "properties": {
                                    "repository": {"type": "string"},
                                    "ref": {"type": "string"},
                                    "count": {"type": "integer", "minimum": 0},
                                    "methods": {
                                        "type": "object",
                                        "description": "Check count per method slug; methods with none are omitted.",
                                        "additionalProperties": {"type": "integer"},
                                    },
                                    "tools": {"type": "array", "items": {"type": "string"}},
                                    "url": {"type": "string", "format": "uri"},
                                },
                            },
                        },
                    },
                },
                "Discussion": {
                    "type": "object",
                    "description": "One review thread an instruction was derived from.",
                    "properties": {
                        "created_at": {"type": "string", "format": "date-time"},
                        "discussion_comments": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "comment_author": {"type": "string"},
                                    "comment_created_at": {
                                        "type": "string",
                                        "format": "date-time",
                                    },
                                },
                            },
                        },
                    },
                },
                "Problem": {
                    "type": "object",
                    "description": "RFC 9457 problem details, with `code` and `resolution` extensions.",
                    "required": ["type", "title", "status"],
                    "properties": {
                        "type": {
                            "type": "string",
                            "format": "uri",
                            "description": "URI identifying the problem type; resolves to its documentation.",
                            "enum": [p["type"] for p in problems],
                        },
                        "title": {"type": "string"},
                        "status": {
                            "type": "integer",
                            "enum": [p["status"] for p in problems],
                        },
                        "detail": {"type": "string"},
                        "instance": {
                            "type": "string",
                            "format": "uri-reference",
                            "description": "The path that produced the error.",
                        },
                        "code": {
                            "type": "string",
                            "description": "Stable machine-readable code for this problem type.",
                            "enum": [p["code"] for p in problems],
                        },
                        "resolution": {
                            "type": "string",
                            "description": "What to do next.",
                        },
                    },
                },
            },
        },
    }


def write_openapi(entries: list[dict], domains: list[dict], version: str) -> None:
    write_json(OPENAPI_PATH, build_openapi(entries, domains, version))


def write_api_data(version: str) -> None:
    """Error descriptions the 404 page renders from."""
    write_json(
        DATA_DIR / "api.json",
        {
            "version": version,
            "openapi": f"{SITE_URL}/openapi.json",
            "resources": DEV_RESOURCES,
            "errors": build_problems(),
        },
    )


def build_llms(entries: list[dict], domains: list[dict], playbooks: list[dict] | None = None) -> list[str]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for entry in entries:
        grouped[entry["domain"]].append(entry)

    lines = [
        "# Awesome Reviewers",
        "",
        "Which checks to run on the code you are writing, and the review prompts for what those",
        "checks miss. Checks come from the CI workflows, pre-commit hooks and task runners of",
        "production open-source repositories; prompts are derived from their code review",
        "discussions. To verify a change: map each changed file to a language with",
        f"{SITE_URL}/raw/verify/index.json, load that language's playbook, run its checks,",
        "then apply its prompts.",
        "",
        f"Corpus: {len(entries)} instructions across {len(domains)} domains.",
        f"Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d')}",
        "",
        "## Awesome Reviewers API — developer resources",
        "",
        "Every endpoint is a static file served over HTTPS: GET only, no key, no rate limit.",
        "",
    ]

    for resource in DEV_RESOURCES:
        lines.append(
            f"- [{resource['name']}]({SITE_URL}{resource['path']}) "
            f"({resource['media_type']}) — {resource['description']}"
        )

    lines += [
        "",
        "Errors follow RFC 9457 problem details, with `code` and `resolution` extension members:",
        "",
    ]
    for problem in build_problems():
        lines.append(
            f"- `{problem['code']}` ({problem['status']}, [{problem['type']}]({problem['type']})) — "
            f"{problem['detail']} {problem['resolution']}"
        )

    lines += [
        "",
        "Markdown variants: an instruction page at /reviewers/<slug>/ is also published as",
        f"{SITE_URL}/raw/<slug>.md, a domain page at /domains/<domain>/ as",
        f"{SITE_URL}/raw/bundles/<domain>.md, and a playbook page at /verify/<language>/ as",
        f"{SITE_URL}/raw/verify/<language>.md. Each HTML page links its markdown variant with",
        "<link rel=\"alternate\" type=\"text/markdown\">.",
        "",
    ]

    if playbooks:
        lines += ["## Verification playbooks", ""]
        for playbook in playbooks:
            lines.append(
                f"- [{playbook['title']}]({playbook['raw_md']}) — files {', '.join(playbook['extensions'])}; "
                f"baseline: {', '.join(playbook['headline']) or 'no tool detected'}"
            )
        lines.append("")

    for domain in domains:
        lines += [
            f"## {domain['title']} ({domain['count']}, updated {domain['updated']})",
            "",
            domain["blurb"],
            "",
            f"Bundle: {SITE_URL}/raw/bundles/{domain['slug']}.md",
            "",
        ]
        for entry in sorted(grouped[domain["slug"]], key=lambda e: e["updated"], reverse=True):
            lines.append(
                f"- [{entry['title']}]({SITE_URL}/raw/{entry['slug']}.md) — "
                f"{entry['repository']}, {entry['topic']}, updated {entry['updated']}"
            )
        lines.append("")

    return lines


def write_llms(entries: list[dict], domains: list[dict], playbooks: list[dict] | None = None) -> None:
    LLMS_PATH.write_text("\n".join(build_llms(entries, domains, playbooks)) + "\n", encoding="utf-8")
    print(f"  wrote {LLMS_PATH} ({LLMS_PATH.stat().st_size / 1024:.0f} KB)")


# --------------------------------------------------------------------------- #


def main() -> None:
    entries = read_corpus()
    if not entries:
        raise SystemExit("no corpus entries found in _reviewers/")

    verifications = read_verifications()
    entries.sort(key=lambda e: (e["updated"], e["comments"]), reverse=True)
    domains = build_domains(entries)
    domain_checks = build_domain_checks(entries, verifications)
    for domain in domains:
        domain["checks"] = domain_checks.get(domain["slug"], [])
    playbooks = build_playbooks(entries, verifications)
    methods = build_methods(entries, verifications)
    catalog = build_catalog(entries, verifications, read_catalog())
    leaderboard = build_leaderboard(entries, verifications, catalog["tactics"])
    source_pages = build_source_pages(entries, verifications)
    playbook_by_slug = {p["slug"]: p for p in playbooks}

    def verify_meta(entry: dict) -> dict:
        # Precomputed so the instruction layout, rendered once per entry, does no lookups.
        playbook = playbook_by_slug.get(language_for_entry(entry) or "")
        page = source_pages.get(repository_slug(entry["repository"])) if entry["repository"] else None
        return {
            "verify": playbook["slug"] if playbook else None,
            "verify_title": playbook["title"] if playbook else None,
            "verify_tools": playbook["headline"] if playbook else [],
            "source": page["slug"] if page else None,
            "source_tools": page["tools"] if page and page["ref"] else None,
        }

    generated = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    print(f"corpus: {len(entries)} instructions, {len(domains)} domains")
    write_json(
        DATA_DIR / "domains.json",
        {
            "generated": generated,
            "updated": max(e["updated"] for e in entries),
            # Jekyll 3's Liquid has no `sum` filter, so totals are precomputed.
            "total": len(entries),
            "repositories": len({e["repository"] for e in entries if e["repository"]}),
            "domains": domains,
        },
    )
    write_json(DATA_DIR / "entries.json", [entry_row(e) for e in entries])
    write_json(
        DATA_DIR / "meta.json",
        {
            e["slug"]: {
                "domain": e["domain"],
                "updated": e["updated"],
                "first_seen": e["first_seen"],
                "discussions": e["discussions"],
                "reviewers": e["authors"][:12],
                **verify_meta(e),
            }
            for e in entries
        },
    )
    write_json(
        DATA_DIR / "sources.json",
        {
            "generated": generated,
            "sources": build_sources(entries, verifications),
            "people": build_people(entries),
        },
    )
    write_search(entries)
    write_domain_pages(domains)
    write_raw(entries, domains, playbooks)
    write_verifications(verifications)
    write_guide(playbooks, methods, source_pages, catalog["tactics"])
    write_catalog(catalog, leaderboard)
    write_llms(entries, domains, playbooks)
    # The corpus date, not the build date: the description only changes when the
    # thing it describes does.
    version = max(e["updated"] for e in entries)
    write_openapi(entries, domains, version)
    write_api_data(version)


if __name__ == "__main__":
    os.chdir(Path(__file__).resolve().parent)
    main()
