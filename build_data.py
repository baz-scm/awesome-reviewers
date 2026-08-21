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
  raw/<page>.md             markdown twin of a prose page (about, contact, …)
  raw/index.json            machine-readable index of the whole corpus
  llms.txt                  domain-grouped index for LLM consumers
  agents.md                 agent instructions: when to use this, and how to call it
  404.md                    the recovery body an agent gets after a bad guess
  openapi.json              OpenAPI 3.1 description of every endpoint
  v1/…                      the versioned JSON surface (see API_VERSION below)
  .well-known/api-catalog   RFC 9727 catalogue pointing at the description above

Everything here is derived. Nothing outside `_reviewers/` is a source of truth,
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
DATA_DIR = Path("_data")
RAW_DIR = Path("raw")
SEARCH_PATH = Path("assets/data/search.json")
LLMS_PATH = Path("llms.txt")
OPENAPI_PATH = Path("openapi.json")
AGENTS_PATH = Path("agents.md")
NOT_FOUND_PATH = Path("404.md")
V1_DIR = Path("v1")
WELL_KNOWN_DIR = Path(".well-known")
API_CATALOG_PATH = WELL_KNOWN_DIR / "api-catalog"
SITE_URL = "https://awesomereviewers.com"
API_DOCS_URL = f"{SITE_URL}/api/"
DEVELOPERS_URL = f"{SITE_URL}/developers/"
REPO_URL = "https://github.com/baz-scm/awesome-reviewers"

# Interface version. It is a path prefix, not a date: `/v1/**` keeps its
# response shapes, and a breaking change ships as `/v2/**` alongside it. The
# corpus date (openapi `info.version`) says how fresh the content is; this says
# what shape it comes in.
API_VERSION = "1"
API_BASE = f"/{V1_DIR}"
API_BASE_URL = f"{SITE_URL}{API_BASE}"
# Days between the Deprecation and Sunset dates of an endpoint being retired.
SUNSET_NOTICE_DAYS = 180
# The quota the edge tier enforces when a rate limiter is bound to it, in the
# structured-field syntax of the RateLimit header fields draft. The static
# origin does not throttle; see build_rate_limit().
RATE_LIMIT_NAME = "default"
RATE_LIMIT_QUOTA = 600
RATE_LIMIT_WINDOW = 60

# Name of the site overview under raw/. No instruction may use it as a slug.
SITE_OVERVIEW_SLUG = "site"
# Prose pages authored as markdown. Each renders as HTML at /<name>/ and is
# published verbatim at /raw/<name>.md, so the page and its markdown twin cannot
# drift. No instruction may use one of these as a slug either.
PROSE_PAGES = ["developers", "about", "contact", "privacy"]
RESERVED_SLUGS = {SITE_OVERVIEW_SLUG, *PROSE_PAGES}

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


def build_sources(entries: list[dict]) -> list[dict]:
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


def build_site_overview(entries: list[dict], domains: list[dict]) -> str:
    """The homepage as markdown: what this is, where everything is, one screen.

    `llms.txt` lists all 5k instructions, which is the wrong thing to hand an
    agent that has just landed on the site. This is the short version, and it is
    what the homepage advertises as its markdown representation.
    """
    lines = [
        "# Awesome Reviewers",
        "",
        "Expert engineering instructions for AI and infrastructure domains, distilled from code",
        "review discussions in production open-source repositories. Each instruction is a",
        "self-contained set of rules you can drop into an agent, harness or context broker as-is.",
        "",
        f"{len(entries)} instructions from "
        f"{len({e['repository'] for e in entries if e['repository']})} repositories, "
        f"across {len(domains)} domains. Last updated "
        f"{max((e['updated'] for e in entries), default='')}.",
        "",
        "## When to use this",
        "",
    ]
    lines += [f"- {item}" for item in WHEN_TO_USE]
    lines += [
        "",
        f"Full agent instructions, including when *not* to use this: {SITE_URL}/agents.md",
        "",
        "## Developer resources",
        "",
        f"Interface version {API_VERSION} ({API_BASE_URL}), {VERSION_POLICY['stability']}. "
        f"GET only, no key, no authentication.",
        "",
    ]
    for resource in DEV_RESOURCES:
        lines.append(
            f"- [{resource['name']}]({SITE_URL}{resource['path']}) "
            f"({resource['media_type']}) — {resource['description']}"
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
        f"RFC 9457 problem details, documented at {API_DOCS_URL}#errors.",
        "",
    ]
    for problem in build_problems():
        lines.append(f"- `{problem['code']}` ({problem['status']}) — {problem['resolution']}")

    lines += ["", "Apache-2.0. Source: https://github.com/baz-scm/awesome-reviewers", ""]
    return "\n".join(lines)


def write_raw(entries: list[dict], domains: list[dict]) -> None:
    if RAW_DIR.exists():
        shutil.rmtree(RAW_DIR)
    (RAW_DIR / "bundles").mkdir(parents=True)

    collisions = sorted(RESERVED_SLUGS.intersection(entry["slug"] for entry in entries))
    if collisions:
        raise SystemExit(
            f"instruction(s) slugged {collisions}, which collide with the reserved "
            f"{RAW_DIR}/<name>.md endpoints; rename the instruction(s)"
        )
    (RAW_DIR / f"{SITE_OVERVIEW_SLUG}.md").write_text(
        build_site_overview(entries, domains), encoding="utf-8"
    )
    write_page_twins()

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
        build_index_payload(
            entries, domains, datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        ),
    )
    print(f"  wrote {len(entries)} raw endpoints and {len(domains)} bundles")


def write_page_twins() -> None:
    """Publish each prose page's own markdown at /raw/<name>.md.

    The page is authored as markdown, so its twin is that same file with the
    front matter cut off: one source, and no way for the two to disagree.
    """
    for name in PROSE_PAGES:
        source = Path(f"{name}.md")
        if not source.exists():
            raise SystemExit(f"{source} is listed in PROSE_PAGES but does not exist")
        meta, body = parse_front_matter(source.read_text(encoding="utf-8"))
        if "{{" in body or "{%" in body:
            raise SystemExit(
                f"{source} contains Liquid, which would be published unrendered in "
                f"{RAW_DIR}/{name}.md; write the URL out instead"
            )
        header = "\n".join(
            [
                "<!--",
                f"title: {meta.get('title', name)}",
                f"url: {SITE_URL}/{name}/",
                "-->",
                "",
                "",
            ]
        )
        title = meta.get("title", name)
        (RAW_DIR / f"{name}.md").write_text(
            f"{header}# {title}\n\n{body}\n", encoding="utf-8"
        )
    print(f"  wrote {len(PROSE_PAGES)} prose page twins")


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
# single source of truth for the API page, llms.txt, agents.md, the api-catalog
# and robots.txt, so an endpoint cannot be added in one place and forgotten in
# the others. `docs: True` marks a page to read rather than an endpoint to call;
# everything else is described in openapi.json.
DEV_RESOURCES: list[dict] = [
    {
        "name": "OpenAPI description",
        "path": "/openapi.json",
        "media_type": "application/vnd.oai.openapi+json;version=3.1",
        "description": "OpenAPI 3.1 description of every endpoint listed here.",
    },
    {
        "name": "API documentation",
        "path": "/api/",
        "media_type": "text/html",
        "description": "Human-readable reference for the endpoints, error format and markdown variants.",
        "docs": True,
    },
    {
        "name": "Developer portal",
        "path": "/developers/",
        "media_type": "text/html",
        "description": "Quickstart, versioning and deprecation policy, rate limits, CLI, sandbox.",
        "docs": True,
    },
    {
        "name": "Agent instructions",
        "path": "/agents.md",
        "media_type": "text/markdown",
        "description": "When to reach for this corpus, when not to, and the call to make for each job.",
    },
    {
        "name": "API catalogue",
        "path": "/.well-known/api-catalog",
        "media_type": "application/linkset+json",
        "description": "RFC 9727 catalogue: one entry per API, linking its description and documentation.",
    },
    {
        "name": "Interface version",
        "path": f"{API_BASE}/version.json",
        "media_type": "application/json",
        "description": "Interface version, lifecycle status, deprecation policy and rate-limit policy.",
    },
    {
        "name": "Corpus index (v1)",
        "path": f"{API_BASE}/index.json",
        "media_type": "application/json",
        "description": "Every instruction with its markdown and JSON URLs. Versioned twin of /raw/index.json.",
    },
    {
        "name": "Domains (v1)",
        "path": f"{API_BASE}/domains.json",
        "media_type": "application/json",
        "description": "One row per domain: blurb, counts, top topics and languages, bundle URL.",
    },
    {
        "name": "Single instruction (v1)",
        "path": f"{API_BASE}/instructions/<slug>.json",
        "media_type": "application/json",
        "description": "One instruction as JSON: every metadata field, the markdown body, and its links.",
    },
    {
        "name": "Error catalogue (v1)",
        "path": f"{API_BASE}/errors/index.json",
        "media_type": "application/json",
        "description": "Every problem type this interface can return, as RFC 9457 problem details.",
    },
    {
        "name": "Error document (v1)",
        "path": f"{API_BASE}/errors/<code>.json",
        "media_type": "application/problem+json",
        "description": "One problem type: its type URI, status, detail and resolution.",
    },
    {
        "name": "Site overview",
        "path": "/raw/site.md",
        "media_type": "text/markdown",
        "description": "The homepage as markdown: what this is, the endpoints, the domains.",
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
    {
        "name": "Recovery body",
        "path": "/404.md",
        "media_type": "text/markdown",
        "description": "What to read after a bad guess: the indexes, the path shapes, the common mistakes.",
    },
    {
        "name": "CLI",
        "path": "/cli/awesome-reviewers.py",
        "media_type": "text/x-python",
        "description": "Single-file CLI over these endpoints: list, get, bundle, search, sync. Python 3.9+, no dependencies.",
    },
]

CLI_PATH = "/cli/awesome-reviewers.py"
CLI_URL = f"{SITE_URL}{CLI_PATH}"

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
    {
        "code": "rate_limited",
        "status": 429,
        "title": "Too many requests",
        "detail": "The quota for this client is exhausted.",
        "resolution": (
            f"Wait for the number of seconds in Retry-After, then retry. The quota is "
            f"{RATE_LIMIT_QUOTA} requests per {RATE_LIMIT_WINDOW} seconds and is reported on "
            f"every response in the RateLimit-Policy and RateLimit header fields. To read the "
            f"whole corpus, fetch one domain bundle instead of every instruction: "
            f"{SITE_URL}/raw/bundles/<domain>.md."
        ),
    },
]

# Machine-readable statements of policy, published at /v1/version.json and
# rendered on /api/ and /developers/. Agents integrate against a surface whose
# change rules they can read, so the rules are part of the interface.
VERSION_POLICY: dict = {
    "scheme": "url-path",
    "current": API_VERSION,
    "base_path": API_BASE,
    "stability": "stable",
    "compatible_changes": [
        "a new endpoint",
        "a new optional field on an existing response",
        "a new domain, topic or language value",
        "new instructions, and new dates on existing ones",
    ],
    "breaking_changes": [
        "removing or renaming a field",
        "changing the type of a field",
        "removing an endpoint",
        "changing the meaning of an existing field",
    ],
    "breaking_change_process": (
        f"A breaking change ships under a new prefix ({SITE_URL}/v2/…) while {API_BASE_URL} keeps "
        f"its response shapes. Nothing is renamed in place."
    ),
    "deprecation": (
        f"A deprecated endpoint answers with the RFC 9745 Deprecation header field, a Link header "
        f"with rel=\"deprecation\" pointing at this policy, and the RFC 8594 Sunset header field "
        f"carrying the date it stops answering — at least {SUNSET_NOTICE_DAYS} days after the "
        f"deprecation date. Live deprecations are listed in the `deprecations` field below, which "
        f"is empty while there are none."
    ),
    "sunset_notice_days": SUNSET_NOTICE_DAYS,
    "documentation": f"{API_DOCS_URL}#versioning",
}


def build_rate_limit() -> dict:
    """The rate-limit policy, and an honest account of who enforces it.

    The origin is a static host with no throttle, so a quota only exists where
    the optional edge worker (`edge/`) is deployed in front of it. Both facts are
    published: the policy an agent should pace itself against, and where it is
    actually applied today.
    """
    return {
        "origin": "none",
        "enforced_by": "edge",
        "policy": f'"{RATE_LIMIT_NAME}";q={RATE_LIMIT_QUOTA};w={RATE_LIMIT_WINDOW}',
        "quota": RATE_LIMIT_QUOTA,
        "window_seconds": RATE_LIMIT_WINDOW,
        "unit": "requests",
        "partition": "client IP address",
        "headers": ["RateLimit-Policy", "RateLimit", "Retry-After"],
        "on_exceeded": {
            "status": 429,
            "problem_type": problem_type_url("rate_limited"),
            "retry_after": "seconds until the window resets",
        },
        # No markdown in here: this string is rendered on an HTML page as well as
        # in JSON and markdown.
        "advice": (
            "Fetch a domain bundle rather than every instruction in it, and diff the updated "
            "date in the index instead of refetching the corpus."
        ),
        "documentation": f"{API_DOCS_URL}#rate-limits",
    }


# Live deprecations, in the shape the edge worker reads to emit Deprecation and
# Sunset headers. Empty while nothing is deprecated, which is the current state.
DEPRECATIONS: list[dict] = []


def problem_type_url(code: str) -> str:
    """The URI an RFC 9457 `type` member points at, resolvable to its docs."""
    return f"{API_DOCS_URL}#error-{code.replace('_', '-')}"


def build_problems() -> list[dict]:
    return [{**problem, "type": problem_type_url(problem["code"])} for problem in PROBLEM_TYPES]


def problem_document_path(code: str) -> str:
    return f"{API_BASE}/errors/{code.replace('_', '-')}.json"


# --------------------------------------------------------------------------- #
# Agent instructions
# --------------------------------------------------------------------------- #

# When to reach for this corpus, when not to, and the call to make. Written once
# here and rendered into agents.md, llms.txt and the developer portal, because an
# agent that lands on any one of them should get the same answer.
WHEN_TO_USE: list[str] = [
    "Reviewing a diff in a subsystem you do not know well — pull the bundle for its domain "
    "and use it as the review rubric.",
    "Assembling or hardening a code-review prompt for one repository or one language — filter "
    "the index by `repository`, `topic` or `language` and paste the matching instructions in.",
    "Building a review harness, skill or context broker that needs review expertise it can gate "
    "by domain, topic or language rather than one generic prompt.",
    "Settling a design argument with what maintainers of comparable systems actually enforce, "
    "with the review threads behind it as evidence.",
    "Onboarding onto an unfamiliar stack: a domain bundle is a readable summary of what reviewers "
    "in that domain keep asking for.",
]

WHEN_NOT_TO_USE: list[str] = [
    "Formatting and style: a linter or formatter is cheaper and exact.",
    "Official guidance about a project — these are distilled from public review threads, not "
    "statements from its maintainers.",
    "The current state of a repository: every instruction carries the date of the newest review "
    "comment behind it, and nothing here is refetched from the source repository at request time.",
    "Anything needing personal data: the corpus holds review discussions and the handles of their "
    "authors, and nothing else.",
]


def call_recipes() -> list[str]:
    """The four calls that cover almost every use of this interface."""
    return [
        f"`GET {API_BASE_URL}/index.json` once per run, then match on `domain`, `topic`, "
        f"`language` or `repository`. It carries the markdown and JSON URL of every instruction.",
        f"`GET {API_BASE_URL}/instructions/<slug>.json` for one instruction as typed JSON "
        f"(metadata, markdown body, provenance links), or `GET {SITE_URL}/raw/<slug>.md` for "
        f"markdown you can paste straight into a prompt.",
        f"`GET {SITE_URL}/raw/bundles/<domain>.md` when you want a whole domain: one request "
        f"instead of one per instruction.",
        f"Poll no more than daily. Compare the `updated` field of each entry against your last "
        f"run instead of refetching the corpus.",
    ]


def build_agents(entries: list[dict], domains: list[dict]) -> str:
    """`/agents.md` — the file to read before calling anything here."""
    problems = build_problems()
    rate_limit = build_rate_limit()
    lines = [
        "# Awesome Reviewers — agent instructions",
        "",
        "Expert engineering instructions for AI and infrastructure domains, distilled from code",
        "review discussions in production open-source repositories. Every endpoint is a static",
        "file served over HTTPS: GET only, no key, no authentication, no personal data.",
        "",
        f"- Corpus: {len(entries)} instructions from "
        f"{len({e['repository'] for e in entries if e['repository']})} repositories across "
        f"{len(domains)} domains, last updated {max((e['updated'] for e in entries), default='')}.",
        f"- Interface version: {API_VERSION} ({API_BASE_URL}), stability "
        f"{VERSION_POLICY['stability']}.",
        f"- Machine description: {SITE_URL}/openapi.json (OpenAPI 3.1).",
        f"- Full index of the corpus: {SITE_URL}/llms.txt.",
        "",
        "## When to use this",
        "",
    ]
    lines += [f"- {item}" for item in WHEN_TO_USE]
    lines += ["", "## When not to use this", ""]
    lines += [f"- {item}" for item in WHEN_NOT_TO_USE]
    lines += ["", "## How to call it", ""]
    lines += [f"{index}. {recipe}" for index, recipe in enumerate(call_recipes(), start=1)]
    lines += [
        "",
        "```bash",
        "# the rubric for one domain, in one request",
        f"curl -sS {SITE_URL}/raw/bundles/llm-infra.md",
        "",
        "# one instruction as JSON, body included",
        f"curl -sS {API_BASE_URL}/instructions/{entries[0]['slug'] if entries else '<slug>'}.json",
        "",
        "# everything in one domain, as slugs",
        f"curl -sS {API_BASE_URL}/index.json \\",
        "  | jq -r '.entries[] | select(.domain == \"orchestration\") | .slug'",
        "```",
        "",
        "## Domains",
        "",
    ]
    for domain in domains:
        lines.append(
            f"- `{domain['slug']}` — {domain['blurb']} ({domain['count']} instructions, "
            f"updated {domain['updated']})"
        )

    lines += [
        "",
        "## Pacing",
        "",
        f"Quota: {rate_limit['quota']} requests per {rate_limit['window_seconds']} seconds per "
        f"{rate_limit['partition']}, advertised in the `RateLimit-Policy` and `RateLimit` header "
        f"fields. {rate_limit['advice']} A 429 carries `Retry-After`; wait that many seconds.",
        "",
        "## Errors",
        "",
        f"RFC 9457 problem details with `code` and `resolution` extension members, documented at "
        f"{API_DOCS_URL}#errors.",
        "",
    ]
    for problem in problems:
        lines.append(
            f"- `{problem['code']}` ({problem['status']}) — {problem['detail']} "
            f"{problem['resolution']}"
        )

    lines += [
        "",
        "## Attribution and licence",
        "",
        "Apache-2.0. Each instruction names the repository it was derived from; keep that "
        "attribution when you redistribute one. The instructions are distilled from public review "
        "discussions and are not official guidance from the projects they came out of.",
        "",
        f"Source: {REPO_URL}",
        "",
    ]
    return "\n".join(lines)


def build_not_found_markdown() -> str:
    """The recovery body for a path that does not exist.

    Served at `/404.md`, embedded in the HTML 404 page, and returned by the edge
    worker to a client that asked for markdown. One text, three places.
    """
    problem = next(p for p in build_problems() if p["code"] == "not_found")
    return "\n".join(
        [
            "# 404 Not Found",
            "",
            f"Nothing is published at this path on Awesome Reviewers. {problem['resolution']}",
            "",
            "## Recover",
            "",
            f"- Corpus index: {SITE_URL}/raw/index.json — every slug, with its raw markdown URL",
            f"- Corpus index (v1): {API_BASE_URL}/index.json — the same rows, with JSON URLs too",
            f"- LLM index: {SITE_URL}/llms.txt — the whole corpus, domain-grouped",
            f"- Agent instructions: {SITE_URL}/agents.md — when to use this, and what to call",
            f"- API description: {SITE_URL}/openapi.json — OpenAPI 3.1",
            f"- API documentation: {API_DOCS_URL}",
            f"- Developer portal: {DEVELOPERS_URL}",
            f"- Sitemap: {SITE_URL}/sitemap.xml",
            "",
            "## Path shapes",
            "",
            "- An instruction is `/reviewers/<slug>/` as a page, `/raw/<slug>.md` as markdown and "
            f"`{API_BASE}/instructions/<slug>.json` as JSON.",
            "- A domain is `/domains/<domain>/` as a page and `/raw/bundles/<domain>.md` as markdown.",
            "- Slugs are lowercase and hyphenated, and only the ones in `/raw/index.json` exist.",
            "",
            "## Problem details",
            "",
            f"- `{problem['code']}` ({problem['status']}) — {problem['type']}",
            f"- Machine-readable: {SITE_URL}{problem_document_path(problem['code'])}",
            "",
        ]
    )


# --------------------------------------------------------------------------- #
# The versioned JSON surface
# --------------------------------------------------------------------------- #


def resource_urls() -> list[dict]:
    """DEV_RESOURCES with absolute URLs, for payloads rather than pages."""
    return [
        {
            "name": resource["name"],
            "url": f"{SITE_URL}{resource['path']}",
            "media_type": resource["media_type"],
            "description": resource["description"],
            "documentation": bool(resource.get("docs")),
        }
        for resource in DEV_RESOURCES
    ]


def build_version(entries: list[dict], version: str, generated: str) -> dict:
    """`/v1/version.json` — what version this is, and what may change when."""
    return {
        "api_version": API_VERSION,
        "base_url": API_BASE_URL,
        "corpus_version": version,
        "generated": generated,
        "count": len(entries),
        "openapi": f"{API_BASE_URL}/openapi.json",
        "documentation": API_DOCS_URL,
        "developer_portal": DEVELOPERS_URL,
        "agent_instructions": f"{SITE_URL}/agents.md",
        "api_catalog": f"{SITE_URL}/{API_CATALOG_PATH.as_posix()}",
        "authentication": "none",
        "versioning": VERSION_POLICY,
        "rate_limit": build_rate_limit(),
        "deprecations": DEPRECATIONS,
        "problem_types": [
            {
                "code": problem["code"],
                "status": problem["status"],
                "type": problem["type"],
                "document": f"{SITE_URL}{problem_document_path(problem['code'])}",
            }
            for problem in build_problems()
        ],
        "resources": resource_urls(),
        "license": {"name": "Apache-2.0", "url": f"{REPO_URL}/blob/main/LICENSE"},
        "source": REPO_URL,
    }


def instruction_urls(slug: str, domain: str) -> dict:
    return {
        "self": f"{API_BASE_URL}/instructions/{slug}.json",
        "page": f"{SITE_URL}/reviewers/{slug}/",
        "markdown": f"{SITE_URL}/raw/{slug}.md",
        "discussions": f"{SITE_URL}/{slug}.json",
        "bundle": f"{SITE_URL}/raw/bundles/{domain}.md",
    }


def build_instruction(entry: dict) -> dict:
    """`/v1/instructions/<slug>.json` — one instruction, body included.

    The markdown endpoint carries the same body behind an HTML comment header;
    this is the variant a typed client can consume without parsing anything.
    """
    return {
        "api_version": API_VERSION,
        "slug": entry["slug"],
        "title": entry["title"],
        "description": entry["description"],
        "repository": entry["repository"],
        "domain": entry["domain"],
        "topic": entry["topic"],
        "language": entry["language"],
        "updated": entry["updated"],
        "first_seen": entry["first_seen"],
        "comments": entry["comments"],
        "discussions": entry["discussions"],
        "stars": entry["stars"],
        "reviewers": entry["authors"][:12],
        "body": entry["body"],
        "media_type": "text/markdown",
        "license": "Apache-2.0",
        "links": instruction_urls(entry["slug"], entry["domain"]),
    }


def build_domains_payload(domains: list[dict], generated: str) -> dict:
    return {
        "api_version": API_VERSION,
        "generated": generated,
        "count": len(domains),
        "domains": [
            {
                "slug": domain["slug"],
                "title": domain["title"],
                "blurb": domain["blurb"],
                "count": domain["count"],
                "repositories": domain["repositories"],
                "updated": domain["updated"],
                "topics": domain["topics"],
                "languages": domain["languages"],
                "bundle": f"{SITE_URL}/raw/bundles/{domain['slug']}.md",
                "page": f"{SITE_URL}/domains/{domain['slug']}/",
            }
            for domain in domains
        ],
    }


def build_index_payload(entries: list[dict], domains: list[dict], generated: str) -> dict:
    """The corpus index. Published unversioned at /raw/index.json and under /v1."""
    return {
        "generated": generated,
        "count": len(entries),
        "site": SITE_URL,
        "api_version": API_VERSION,
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
            {
                **entry_row(e),
                "raw": f"{SITE_URL}/raw/{e['slug']}.md",
                "json": f"{API_BASE_URL}/instructions/{e['slug']}.json",
            }
            for e in entries
        ],
    }


def build_api_catalog() -> dict:
    """`/.well-known/api-catalog` — RFC 9727, in the RFC 9264 linkset format.

    One API, so one item: the versioned interface, with its description, its
    documentation and its version metadata hung off it.
    """
    return {
        "linkset": [
            {
                "anchor": f"{SITE_URL}/{API_CATALOG_PATH.as_posix()}",
                "item": [
                    {
                        "href": API_BASE_URL,
                        "title": f"Awesome Reviewers API v{API_VERSION}",
                        "type": "application/json",
                    }
                ],
                "describedby": [
                    {
                        "href": "https://www.rfc-editor.org/info/rfc9727",
                        "type": "text/html",
                        "title": "RFC 9727 — API catalogue",
                    }
                ],
            },
            {
                "anchor": API_BASE_URL,
                "service-desc": [
                    {
                        "href": f"{SITE_URL}/openapi.json",
                        "type": "application/vnd.oai.openapi+json;version=3.1",
                        "title": "OpenAPI 3.1 description",
                    }
                ],
                "service-doc": [
                    {"href": API_DOCS_URL, "type": "text/html", "title": "API documentation"},
                    {
                        "href": DEVELOPERS_URL,
                        "type": "text/html",
                        "title": "Developer portal",
                    },
                ],
                "service-meta": [
                    {
                        "href": f"{API_BASE_URL}/version.json",
                        "type": "application/json",
                        "title": "Interface version, versioning and rate-limit policy",
                    },
                    {
                        "href": f"{SITE_URL}/agents.md",
                        "type": "text/markdown",
                        "title": "Agent instructions",
                    },
                ],
                "license": [
                    {
                        "href": "https://www.apache.org/licenses/LICENSE-2.0",
                        "title": "Apache-2.0",
                    }
                ],
            },
        ]
    }


def build_openapi(entries: list[dict], domains: list[dict], version: str) -> dict:
    """OpenAPI 3.1 description of the static endpoints the site publishes.

    Everything here is a plain file served over HTTP: no key, no rate limit and
    no method other than GET. The description exists so an agent can discover
    the shape of the corpus without scraping the HTML.
    """
    example_slug = entries[0]["slug"] if entries else "example-instruction"
    domain_slugs = [d["slug"] for d in domains]
    problems = build_problems()

    def error_response(status: int) -> dict:
        problem = next(p for p in problems if p["status"] == status)
        headers = {"RateLimit-Policy": {"$ref": "#/components/headers/RateLimitPolicy"}}
        if status == 429:
            headers = {
                "Retry-After": {"$ref": "#/components/headers/RetryAfter"},
                "RateLimit": {"$ref": "#/components/headers/RateLimit"},
                "RateLimit-Policy": {"$ref": "#/components/headers/RateLimitPolicy"},
            }
        return {
            "description": problem["title"],
            "headers": headers,
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
            "headers": {"RateLimit-Policy": {"$ref": "#/components/headers/RateLimitPolicy"}},
        }

    def json_response(description: str, schema: str) -> dict:
        return {
            "description": description,
            "content": {"application/json": {"schema": {"$ref": f"#/components/schemas/{schema}"}}},
            "headers": {"RateLimit-Policy": {"$ref": "#/components/headers/RateLimitPolicy"}},
        }

    rate_limit = build_rate_limit()

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
                "Every endpoint is a static file served over HTTPS. There is no key, no "
                "authentication and no method other than GET. Responses are immutable for a given "
                "build; the `updated` field on each entry carries the date of the most recent "
                "review comment behind it, so a scheduled job can diff against its last run "
                "instead of refetching the corpus.\n\n"
                f"**Versioning.** The interface is versioned in the URL path: `{API_BASE}/**` "
                f"keeps its response shapes, and a breaking change ships as `/v2/**` beside it "
                f"rather than replacing anything. `info.version` above is the corpus date — how "
                f"fresh the content is; `x-api-version` is the interface version — what shape it "
                f"comes in. Unversioned paths (`/raw/**`, `/llms.txt`) predate the prefix and are "
                f"maintained as aliases of the v1 shapes. A retiring endpoint answers with the "
                f"RFC 9745 `Deprecation` and RFC 8594 `Sunset` header fields at least "
                f"{SUNSET_NOTICE_DAYS} days apart, plus a `Link` with `rel=\"deprecation\"`. The "
                f"live policy and the current (empty) deprecation list are published at "
                f"`{API_BASE}/version.json`.\n\n"
                f"**Pacing.** The static origin does not throttle. Where the optional edge tier is "
                f"deployed it enforces `{rate_limit['policy']}` per {rate_limit['partition']} and "
                f"reports it in the `RateLimit-Policy` and `RateLimit` header fields; a 429 "
                f"carries `Retry-After`. {rate_limit['advice']}\n\n"
                "**Errors.** RFC 9457 problem details, with `code` and `resolution` extension "
                f"members. Each type is also published as a document under `{API_BASE}/errors/`."
            ),
            "termsOfService": f"{API_DOCS_URL}#terms",
            "contact": {
                "name": "Awesome Reviewers",
                "url": REPO_URL,
            },
            "license": {
                "name": "Apache-2.0",
                "identifier": "Apache-2.0",
            },
        },
        "x-api-version": API_VERSION,
        "x-versioning": VERSION_POLICY,
        "x-rate-limit": rate_limit,
        "externalDocs": {
            "description": "Awesome Reviewers API documentation",
            "url": API_DOCS_URL,
        },
        "servers": [{"url": SITE_URL, "description": "Production"}],
        "tags": [
            {"name": "instructions", "description": "Single instructions and domain bundles."},
            {"name": "indexes", "description": "Machine-readable indexes of the whole corpus."},
            {"name": "discovery", "description": "Descriptions of the site itself."},
            {"name": "errors", "description": "The problem types this interface can return."},
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
                        "200": json_response("The corpus index", "Index"),
                        "404": error_response(404),
                        "429": error_response(429),
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
                        "429": error_response(429),
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
                        "429": error_response(429),
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
                        "429": error_response(429),
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
                            "headers": {
                                "RateLimit-Policy": {
                                    "$ref": "#/components/headers/RateLimitPolicy"
                                }
                            },
                        },
                        "404": error_response(404),
                        "429": error_response(429),
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
                        "200": json_response("The search index", "SearchIndex"),
                        "404": error_response(404),
                        "429": error_response(429),
                    },
                }
            },
            "/llms.txt": {
                "get": {
                    "operationId": "getLlmsTxt",
                    "summary": "Domain-grouped index of the corpus for LLM consumers",
                    "description": (
                        "The whole corpus as plain text: what this is, when to use it, the "
                        "developer resources, the error format, then every instruction grouped by "
                        "domain with its markdown URL. Around 900 KB — prefer /raw/site.md to "
                        "orient, and the index to filter."
                    ),
                    "tags": ["indexes"],
                    "responses": {
                        "200": {
                            "description": "The llms.txt index",
                            "content": {"text/plain": {"schema": {"type": "string"}}},
                        },
                        "404": error_response(404),
                        "429": error_response(429),
                    },
                }
            },
            "/openapi.json": {
                "get": {
                    "operationId": "getOpenapi",
                    "summary": "This description",
                    "description": (
                        "The OpenAPI 3.1 description of every endpoint here, linked from every "
                        "page as rel=\"service-desc\" and from the API catalogue."
                    ),
                    "tags": ["discovery"],
                    "responses": {
                        "200": {
                            "description": "The OpenAPI description",
                            "content": {
                                "application/vnd.oai.openapi+json;version=3.1": {
                                    "schema": {"type": "object"}
                                }
                            },
                        },
                        "429": error_response(429),
                    },
                }
            },
            "/sitemap.xml": {
                "get": {
                    "operationId": "getSitemap",
                    "summary": "Every HTML page on the site",
                    "description": (
                        "The sitemap the site advertises in robots.txt. Pages only: the raw "
                        "endpoints are indexed in /raw/index.json instead."
                    ),
                    "tags": ["discovery"],
                    "responses": {
                        "200": {
                            "description": "The sitemap",
                            "content": {"application/xml": {"schema": {"type": "string"}}},
                        },
                        "429": error_response(429),
                    },
                }
            },
            f"{API_BASE}/version.json": {
                "get": {
                    "operationId": "getVersion",
                    "summary": "Interface version, versioning policy and rate-limit policy",
                    "description": (
                        "What version this interface is, what counts as a breaking change, how a "
                        "retiring endpoint is signalled, what the quota is, and every other "
                        "resource published here. Read this first if you are integrating."
                    ),
                    "tags": ["discovery"],
                    "responses": {
                        "200": json_response("The interface version", "Version"),
                        "429": error_response(429),
                    },
                }
            },
            f"{API_BASE}/openapi.json": {
                "get": {
                    "operationId": "getOpenapiV1",
                    "summary": "This description, under the version prefix",
                    "description": (
                        f"Byte-identical to /openapi.json, published under {API_BASE} so the "
                        f"versioned surface is self-contained."
                    ),
                    "tags": ["discovery"],
                    "responses": {
                        "200": {
                            "description": "The OpenAPI description",
                            "content": {
                                "application/vnd.oai.openapi+json;version=3.1": {
                                    "schema": {"type": "object"}
                                }
                            },
                        },
                        "429": error_response(429),
                    },
                }
            },
            f"{API_BASE}/index.json": {
                "get": {
                    "operationId": "getIndexV1",
                    "summary": "Machine-readable index of the whole corpus, versioned",
                    "description": (
                        "The same rows as /raw/index.json, with a `json` field on each entry "
                        "pointing at its typed representation. This is the entry point: fetch it "
                        "once, cache it, and match on domain, topic, language or repository."
                    ),
                    "tags": ["indexes"],
                    "responses": {
                        "200": json_response("The corpus index", "Index"),
                        "429": error_response(429),
                    },
                }
            },
            f"{API_BASE}/domains.json": {
                "get": {
                    "operationId": "getDomains",
                    "summary": "Every domain, with its counts and bundle URL",
                    "description": (
                        "One row per domain: blurb, instruction and repository counts, its most "
                        "common topics and languages, and the URL of its markdown bundle."
                    ),
                    "tags": ["indexes"],
                    "responses": {
                        "200": json_response("The domains", "DomainList"),
                        "429": error_response(429),
                    },
                }
            },
            f"{API_BASE}/facets.json": {
                "get": {
                    "operationId": "getFacets",
                    "summary": "Every topic, language and repository, with counts",
                    "description": (
                        "The values the index can be filtered by, each with the number of "
                        "instructions carrying it. Use it to gate a review harness by topic or "
                        "language without scanning the index."
                    ),
                    "tags": ["indexes"],
                    "responses": {
                        "200": json_response("The facets", "Facets"),
                        "429": error_response(429),
                    },
                }
            },
            f"{API_BASE}/sources.json": {
                "get": {
                    "operationId": "getSources",
                    "summary": "Every source repository, with counts and reviewer totals",
                    "description": (
                        "One row per repository the corpus was derived from: how many "
                        "instructions came out of it, how many reviewers are behind them, its "
                        "domain and the date of its most recent review comment."
                    ),
                    "tags": ["indexes"],
                    "responses": {
                        "200": json_response("The source repositories", "SourceList"),
                        "429": error_response(429),
                    },
                }
            },
            f"{API_BASE}/instructions/{{slug}}.json": {
                "get": {
                    "operationId": "getInstructionJson",
                    "summary": "One instruction as JSON, body included",
                    "description": (
                        "Every metadata field, the markdown body, the reviewers whose comments it "
                        "was distilled from, and links to its page, its markdown and its source "
                        "discussions. The typed alternative to /raw/{slug}.md."
                    ),
                    "tags": ["instructions"],
                    "parameters": [{"$ref": "#/components/parameters/Slug"}],
                    "responses": {
                        "200": json_response("The instruction", "Instruction"),
                        "404": error_response(404),
                        "429": error_response(429),
                    },
                }
            },
            f"{API_BASE}/errors/index.json": {
                "get": {
                    "operationId": "getErrorCatalog",
                    "summary": "Every problem type this interface can return",
                    "description": (
                        "The error catalogue: one entry per problem type, each with its type URI, "
                        "status, detail, resolution and the URL of its own document."
                    ),
                    "tags": ["errors"],
                    "responses": {
                        "200": json_response("The error catalogue", "ProblemCatalog"),
                        "429": error_response(429),
                    },
                }
            },
            f"{API_BASE}/errors/{{code}}.json": {
                "get": {
                    "operationId": "getErrorDocument",
                    "summary": "One problem type as a document",
                    "description": (
                        "The problem details for one error, without having to provoke it. Served "
                        "as application/json because it is a description rather than an error; a "
                        "real error carries the same body as application/problem+json."
                    ),
                    "tags": ["errors"],
                    "parameters": [
                        {
                            "name": "code",
                            "in": "path",
                            "required": True,
                            "description": "Problem code, hyphenated.",
                            "schema": {
                                "type": "string",
                                "enum": [p["code"].replace("_", "-") for p in problems],
                            },
                            "example": problems[0]["code"].replace("_", "-"),
                        }
                    ],
                    "responses": {
                        "200": json_response("The problem type", "Problem"),
                        "404": error_response(404),
                        "429": error_response(429),
                    },
                }
            },
            "/.well-known/api-catalog": {
                "get": {
                    "operationId": "getApiCatalog",
                    "summary": "RFC 9727 catalogue of the APIs published here",
                    "description": (
                        "A linkset (RFC 9264) naming this API and linking its description, its "
                        "documentation and its version metadata. Static hosting cannot set the "
                        "`profile` media-type parameter RFC 9727 recommends; the edge tier does, "
                        "and the catalogue links RFC 9727 as `describedby` either way."
                    ),
                    "tags": ["discovery"],
                    "responses": {
                        "200": {
                            "description": "The API catalogue",
                            "content": {
                                "application/linkset+json": {
                                    "schema": {"$ref": "#/components/schemas/Linkset"}
                                }
                            },
                        },
                        "429": error_response(429),
                    },
                }
            },
            "/agents.md": {
                "get": {
                    "operationId": "getAgentInstructions",
                    "summary": "When to use this corpus, when not to, and what to call",
                    "description": (
                        "Agent instructions: the jobs this corpus is right for, the jobs it is "
                        "wrong for, the four calls that cover almost every use, the domain list, "
                        "the pacing advice and the error catalogue."
                    ),
                    "tags": ["discovery"],
                    "responses": {
                        "200": markdown_response("The agent instructions"),
                        "429": error_response(429),
                    },
                }
            },
            "/404.md": {
                "get": {
                    "operationId": "getRecoveryBody",
                    "summary": "The recovery body for a path that does not exist",
                    "description": (
                        "What to read after a bad guess: the indexes, the path shapes, the common "
                        "mistakes. The HTML 404 page carries the same text, and the edge tier "
                        "returns it with a 404 status to a client that asked for markdown."
                    ),
                    "tags": ["errors"],
                    "responses": {
                        "200": markdown_response("The recovery body"),
                        "429": error_response(429),
                    },
                }
            },
            CLI_PATH: {
                "get": {
                    "operationId": "getCli",
                    "summary": "The CLI as a single file",
                    "description": (
                        "A dependency-free Python 3.9+ script over these endpoints: list, get, "
                        "bundle, search and sync. Download it, chmod +x it, run it."
                    ),
                    "tags": ["discovery"],
                    "responses": {
                        "200": {
                            "description": "The CLI script",
                            "content": {"text/x-python": {"schema": {"type": "string"}}},
                        },
                        "429": error_response(429),
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
            "headers": {
                "RateLimitPolicy": {
                    "description": (
                        "The quota this interface advertises, in the structured-field syntax of "
                        "the RateLimit header fields specification. Present where the edge tier "
                        "is deployed; the static origin does not throttle."
                    ),
                    "required": False,
                    "schema": {"type": "string"},
                    "example": rate_limit["policy"],
                },
                "RateLimit": {
                    "description": (
                        "Quota left in the current window: `r` is the remaining allowance, `t` "
                        "the seconds until it resets."
                    ),
                    "required": False,
                    "schema": {"type": "string"},
                    "example": f'"{RATE_LIMIT_NAME}";r=0;t={RATE_LIMIT_WINDOW}',
                },
                "RetryAfter": {
                    "description": "Seconds to wait before retrying. Takes precedence over `t`.",
                    "required": False,
                    "schema": {"type": "integer", "minimum": 0},
                    "example": RATE_LIMIT_WINDOW,
                },
                "Deprecation": {
                    "description": (
                        "RFC 9745. Present only on a deprecated endpoint, carrying the date the "
                        "deprecation took effect; paired with Sunset and a Link with "
                        'rel="deprecation".'
                    ),
                    "required": False,
                    "schema": {"type": "string"},
                    "example": "@1788134400",
                },
                "Sunset": {
                    "description": (
                        f"RFC 8594. The date a deprecated endpoint stops answering, never less "
                        f"than {SUNSET_NOTICE_DAYS} days after the Deprecation date."
                    ),
                    "required": False,
                    "schema": {"type": "string"},
                    "example": "Wed, 01 Jul 2026 00:00:00 GMT",
                },
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
                        "json": {
                            "type": "string",
                            "format": "uri",
                            "description": "URL of this instruction as JSON, body included.",
                        },
                    },
                },
                "Instruction": {
                    "type": "object",
                    "description": "One instruction, with its markdown body and its links.",
                    "required": ["api_version", "slug", "title", "body", "links"],
                    "properties": {
                        "api_version": {"type": "string", "const": API_VERSION},
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
                        "first_seen": {
                            "type": "string",
                            "format": "date",
                            "description": "Date of the oldest review comment behind it.",
                        },
                        "comments": {"type": "integer", "minimum": 0},
                        "discussions": {
                            "type": "integer",
                            "minimum": 0,
                            "description": "Number of review threads it was distilled from.",
                        },
                        "stars": {"type": "integer", "minimum": 0},
                        "reviewers": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Handles of the reviewers whose comments it came from.",
                        },
                        "body": {
                            "type": "string",
                            "description": "The instruction itself, as markdown.",
                        },
                        "media_type": {"type": "string", "const": "text/markdown"},
                        "license": {"type": "string", "const": "Apache-2.0"},
                        "links": {
                            "type": "object",
                            "description": "Every other representation of this instruction.",
                            "required": ["self", "page", "markdown"],
                            "properties": {
                                "self": {"type": "string", "format": "uri"},
                                "page": {"type": "string", "format": "uri"},
                                "markdown": {"type": "string", "format": "uri"},
                                "discussions": {"type": "string", "format": "uri"},
                                "bundle": {"type": "string", "format": "uri"},
                            },
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
                        "api_version": {"type": "string", "const": API_VERSION},
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
                "DomainList": {
                    "type": "object",
                    "description": "Every domain, with counts and its bundle URL.",
                    "required": ["api_version", "count", "domains"],
                    "properties": {
                        "api_version": {"type": "string", "const": API_VERSION},
                        "generated": {"type": "string", "format": "date-time"},
                        "count": {"type": "integer", "minimum": 0},
                        "domains": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "required": ["slug", "title", "count", "bundle"],
                                "properties": {
                                    "slug": {"type": "string", "enum": domain_slugs},
                                    "title": {"type": "string"},
                                    "blurb": {"type": "string"},
                                    "count": {"type": "integer", "minimum": 0},
                                    "repositories": {"type": "integer", "minimum": 0},
                                    "updated": {"type": "string", "format": "date"},
                                    "topics": {"type": "array", "items": {"type": "string"}},
                                    "languages": {"type": "array", "items": {"type": "string"}},
                                    "bundle": {"type": "string", "format": "uri"},
                                    "page": {"type": "string", "format": "uri"},
                                },
                            },
                        },
                    },
                },
                "Facet": {
                    "type": "object",
                    "description": "One filterable value and how many instructions carry it.",
                    "required": ["value", "count"],
                    "properties": {
                        "value": {"type": "string"},
                        "count": {"type": "integer", "minimum": 1},
                    },
                },
                "Facets": {
                    "type": "object",
                    "description": "The values the index can be filtered by.",
                    "required": ["api_version", "topics", "languages", "repositories"],
                    "properties": {
                        "api_version": {"type": "string", "const": API_VERSION},
                        "generated": {"type": "string", "format": "date-time"},
                        "domains": {
                            "type": "array",
                            "items": {"$ref": "#/components/schemas/Facet"},
                        },
                        "topics": {
                            "type": "array",
                            "items": {"$ref": "#/components/schemas/Facet"},
                        },
                        "languages": {
                            "type": "array",
                            "items": {"$ref": "#/components/schemas/Facet"},
                        },
                        "repositories": {
                            "type": "array",
                            "items": {"$ref": "#/components/schemas/Facet"},
                        },
                    },
                },
                "SourceList": {
                    "type": "object",
                    "description": "Every repository the corpus was derived from.",
                    "required": ["api_version", "count", "sources"],
                    "properties": {
                        "api_version": {"type": "string", "const": API_VERSION},
                        "generated": {"type": "string", "format": "date-time"},
                        "count": {"type": "integer", "minimum": 0},
                        "sources": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "required": ["repository", "count", "domain"],
                                "properties": {
                                    "repository": {"type": "string"},
                                    "count": {"type": "integer", "minimum": 1},
                                    "stars": {"type": "integer", "minimum": 0},
                                    "domain": {"type": "string", "enum": domain_slugs},
                                    "updated": {"type": "string", "format": "date"},
                                    "reviewers": {"type": "integer", "minimum": 0},
                                    "url": {"type": "string", "format": "uri"},
                                },
                            },
                        },
                    },
                },
                "Version": {
                    "type": "object",
                    "description": (
                        "The interface version, its lifecycle rules and its quota. The document to "
                        "read before integrating."
                    ),
                    "required": ["api_version", "base_url", "corpus_version", "versioning"],
                    "properties": {
                        "api_version": {"type": "string", "const": API_VERSION},
                        "base_url": {"type": "string", "format": "uri"},
                        "corpus_version": {
                            "type": "string",
                            "format": "date",
                            "description": "Date of the newest review comment in the corpus.",
                        },
                        "generated": {"type": "string", "format": "date-time"},
                        "count": {"type": "integer", "minimum": 0},
                        "openapi": {"type": "string", "format": "uri"},
                        "documentation": {"type": "string", "format": "uri"},
                        "developer_portal": {"type": "string", "format": "uri"},
                        "agent_instructions": {"type": "string", "format": "uri"},
                        "api_catalog": {"type": "string", "format": "uri"},
                        "authentication": {"type": "string", "const": "none"},
                        "versioning": {
                            "type": "object",
                            "description": "What may change, when, and how it is signalled.",
                            "required": ["scheme", "current", "base_path", "stability"],
                            "properties": {
                                "scheme": {"type": "string", "const": "url-path"},
                                "current": {"type": "string"},
                                "base_path": {"type": "string"},
                                "stability": {
                                    "type": "string",
                                    "enum": ["experimental", "beta", "stable", "deprecated"],
                                },
                                "compatible_changes": {
                                    "type": "array",
                                    "items": {"type": "string"},
                                },
                                "breaking_changes": {
                                    "type": "array",
                                    "items": {"type": "string"},
                                },
                                "breaking_change_process": {"type": "string"},
                                "deprecation": {"type": "string"},
                                "sunset_notice_days": {"type": "integer", "minimum": 0},
                                "documentation": {"type": "string", "format": "uri"},
                            },
                        },
                        "rate_limit": {
                            "type": "object",
                            "description": "The advertised quota, and who applies it.",
                            "required": ["policy", "quota", "window_seconds", "enforced_by"],
                            "properties": {
                                "origin": {"type": "string"},
                                "enforced_by": {"type": "string"},
                                "policy": {"type": "string", "example": rate_limit["policy"]},
                                "quota": {"type": "integer", "minimum": 1},
                                "window_seconds": {"type": "integer", "minimum": 1},
                                "unit": {"type": "string"},
                                "partition": {"type": "string"},
                                "headers": {"type": "array", "items": {"type": "string"}},
                                "on_exceeded": {"type": "object"},
                                "advice": {"type": "string"},
                                "documentation": {"type": "string", "format": "uri"},
                            },
                        },
                        "deprecations": {
                            "type": "array",
                            "description": (
                                "Endpoints being retired. Empty while there are none. Each entry "
                                "carries the path, the deprecation and sunset dates, and the "
                                "successor to move to."
                            ),
                            "items": {
                                "type": "object",
                                "required": ["path", "deprecation", "sunset"],
                                "properties": {
                                    "path": {"type": "string"},
                                    "deprecation": {"type": "string", "format": "date"},
                                    "sunset": {"type": "string", "format": "date"},
                                    "successor": {"type": "string"},
                                    "reason": {"type": "string"},
                                },
                            },
                        },
                        "problem_types": {"type": "array", "items": {"type": "object"}},
                        "resources": {
                            "type": "array",
                            "description": "Every resource published here, with its media type.",
                            "items": {
                                "type": "object",
                                "required": ["name", "url", "media_type"],
                                "properties": {
                                    "name": {"type": "string"},
                                    "url": {"type": "string", "format": "uri"},
                                    "media_type": {"type": "string"},
                                    "description": {"type": "string"},
                                    "documentation": {"type": "boolean"},
                                },
                            },
                        },
                        "license": {"type": "object"},
                        "source": {"type": "string", "format": "uri"},
                    },
                },
                "ProblemCatalog": {
                    "type": "object",
                    "description": "Every problem type this interface can return.",
                    "required": ["api_version", "count", "errors"],
                    "properties": {
                        "api_version": {"type": "string", "const": API_VERSION},
                        "count": {"type": "integer", "minimum": 0},
                        "documentation": {"type": "string", "format": "uri"},
                        "errors": {
                            "type": "array",
                            "items": {"$ref": "#/components/schemas/Problem"},
                        },
                    },
                },
                "Linkset": {
                    "type": "object",
                    "description": "An RFC 9264 linkset: link contexts, each keyed by relation.",
                    "required": ["linkset"],
                    "properties": {
                        "linkset": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "required": ["anchor"],
                                "properties": {"anchor": {"type": "string", "format": "uri"}},
                                "additionalProperties": True,
                            },
                        }
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
    """Machine interface description the API page renders from."""
    write_json(
        DATA_DIR / "api.json",
        {
            "version": version,
            "api_version": API_VERSION,
            "base_url": API_BASE_URL,
            "base_path": API_BASE,
            "openapi": f"{SITE_URL}/openapi.json",
            "catalog": f"{SITE_URL}/{API_CATALOG_PATH.as_posix()}",
            "agents": f"{SITE_URL}/agents.md",
            "cli": CLI_URL,
            "resources": DEV_RESOURCES,
            "errors": build_problems(),
            "versioning": VERSION_POLICY,
            "rate_limit": build_rate_limit(),
            "deprecations": DEPRECATIONS,
            # The recovery text the 404 page renders, so the page and /404.md
            # cannot say different things.
            "not_found_markdown": build_not_found_markdown(),
            "when_to_use": WHEN_TO_USE,
            "when_not_to_use": WHEN_NOT_TO_USE,
            "call_recipes": call_recipes(),
        },
    )


def build_facets(entries: list[dict], domains: list[dict]) -> dict:
    """Every value the index can be filtered by, with its instruction count."""

    def counted(values: list[str]) -> list[dict]:
        counter = Counter(value for value in values if value)
        return [
            {"value": value, "count": count}
            for value, count in sorted(counter.items(), key=lambda pair: (-pair[1], pair[0]))
        ]

    titles = {d["slug"]: d["title"] for d in domains}
    return {
        "api_version": API_VERSION,
        "generated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "domains": [
            {"value": domain["slug"], "count": domain["count"], "title": titles[domain["slug"]]}
            for domain in domains
        ],
        "topics": counted([e["topic"] for e in entries]),
        "languages": counted([e["language"] for e in entries]),
        "repositories": counted([e["repository"] for e in entries]),
    }


def build_sources_payload(entries: list[dict], generated: str) -> dict:
    sources = build_sources(entries)
    return {
        "api_version": API_VERSION,
        "generated": generated,
        "count": len(sources),
        "sources": [
            {**source, "url": f"https://github.com/{source['repository']}"} for source in sources
        ],
    }


def write_v1(entries: list[dict], domains: list[dict], version: str, generated: str) -> None:
    """The versioned JSON surface: `/v1/**`.

    Everything here is derived from the same corpus the markdown endpoints are,
    and the shapes are the ones openapi.json describes. The prefix is the
    contract: a breaking change ships as `/v2/**` rather than editing these.
    """
    if V1_DIR.exists():
        shutil.rmtree(V1_DIR)
    (V1_DIR / "instructions").mkdir(parents=True)
    (V1_DIR / "errors").mkdir(parents=True)

    write_json(V1_DIR / "version.json", build_version(entries, version, generated))
    write_json(V1_DIR / "index.json", build_index_payload(entries, domains, generated))
    write_json(V1_DIR / "domains.json", build_domains_payload(domains, generated))
    write_json(V1_DIR / "facets.json", build_facets(entries, domains))
    write_json(V1_DIR / "sources.json", build_sources_payload(entries, generated))
    write_json(V1_DIR / "openapi.json", build_openapi(entries, domains, version))

    problems = build_problems()
    write_json(
        V1_DIR / "errors" / "index.json",
        {
            "api_version": API_VERSION,
            "count": len(problems),
            "documentation": f"{API_DOCS_URL}#errors",
            "errors": problems,
        },
    )
    for problem in problems:
        write_json(V1_DIR / "errors" / f"{problem['code'].replace('_', '-')}.json", problem)

    for entry in entries:
        path = V1_DIR / "instructions" / f"{entry['slug']}.json"
        with path.open("w", encoding="utf-8") as handle:
            json.dump(build_instruction(entry), handle, ensure_ascii=False, separators=(",", ":"))
            handle.write("\n")
    print(f"  wrote {len(entries)} instruction documents under {V1_DIR}/instructions")


def write_well_known() -> None:
    """`/.well-known/api-catalog`, per RFC 9727."""
    WELL_KNOWN_DIR.mkdir(exist_ok=True)
    write_json(API_CATALOG_PATH, build_api_catalog())


def write_agents(entries: list[dict], domains: list[dict]) -> None:
    AGENTS_PATH.write_text(build_agents(entries, domains), encoding="utf-8")
    print(f"  wrote {AGENTS_PATH}")


def write_not_found() -> None:
    NOT_FOUND_PATH.write_text(build_not_found_markdown(), encoding="utf-8")
    print(f"  wrote {NOT_FOUND_PATH}")


def build_llms(entries: list[dict], domains: list[dict]) -> list[str]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for entry in entries:
        grouped[entry["domain"]].append(entry)

    lines = [
        "# Awesome Reviewers",
        "",
        "Expert engineering instructions for AI and infrastructure domains, derived from",
        "code review discussions in production open-source repositories. Each instruction",
        "is a self-contained set of rules you can drop into an agent, harness or context",
        "broker as-is.",
        "",
        f"Corpus: {len(entries)} instructions across {len(domains)} domains.",
        f"Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d')}",
        "",
        "## When to use Awesome Reviewers",
        "",
    ]
    lines += [f"- {item}" for item in WHEN_TO_USE]
    lines += ["", "## When not to use it", ""]
    lines += [f"- {item}" for item in WHEN_NOT_TO_USE]
    lines += ["", "## How to call it", ""]
    lines += [f"{index}. {recipe}" for index, recipe in enumerate(call_recipes(), start=1)]
    lines += [
        "",
        f"Full agent instructions: {SITE_URL}/agents.md",
        "",
        "## Awesome Reviewers API — developer resources",
        "",
        "Every endpoint is a static file served over HTTPS: GET only, no key, no authentication.",
        f"Interface version {API_VERSION} ({API_BASE_URL}), {VERSION_POLICY['stability']}. "
        f"Versioning and deprecation policy: {API_BASE_URL}/version.json.",
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

    rate_limit = build_rate_limit()
    lines += [
        "",
        f"Pacing: {rate_limit['quota']} requests per {rate_limit['window_seconds']} seconds, "
        f"advertised in the RateLimit-Policy and",
        "RateLimit header fields. A 429 carries Retry-After. Fetch a domain bundle rather than",
        "every instruction in it.",
        "",
        "Markdown variants: an instruction page at /reviewers/<slug>/ is also published as",
        f"{SITE_URL}/raw/<slug>.md and as {API_BASE_URL}/instructions/<slug>.json, a domain page",
        f"at /domains/<domain>/ as {SITE_URL}/raw/bundles/<domain>.md, and each prose page",
        f"(/developers/, /about/, /contact/, /privacy/) as {SITE_URL}/raw/<page>.md. Each HTML page",
        "links its variants with <link rel=\"alternate\" type=\"text/markdown\"> and, where there is",
        "one, <link rel=\"alternate\" type=\"application/json\">.",
        "",
    ]

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


def write_llms(entries: list[dict], domains: list[dict]) -> None:
    LLMS_PATH.write_text("\n".join(build_llms(entries, domains)) + "\n", encoding="utf-8")
    print(f"  wrote {LLMS_PATH} ({LLMS_PATH.stat().st_size / 1024:.0f} KB)")


# --------------------------------------------------------------------------- #


def main() -> None:
    entries = read_corpus()
    if not entries:
        raise SystemExit("no corpus entries found in _reviewers/")

    entries.sort(key=lambda e: (e["updated"], e["comments"]), reverse=True)
    domains = build_domains(entries)
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
            }
            for e in entries
        },
    )
    write_json(
        DATA_DIR / "sources.json",
        {
            "generated": generated,
            "sources": build_sources(entries),
            "people": build_people(entries),
        },
    )
    write_search(entries)
    write_domain_pages(domains)
    write_raw(entries, domains)
    write_llms(entries, domains)
    write_agents(entries, domains)
    write_not_found()
    # The corpus date, not the build date: the description only changes when the
    # thing it describes does.
    version = max(e["updated"] for e in entries)
    write_openapi(entries, domains, version)
    write_v1(entries, domains, version, generated)
    write_well_known()
    write_api_data(version)


if __name__ == "__main__":
    os.chdir(Path(__file__).resolve().parent)
    main()
