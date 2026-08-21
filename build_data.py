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
  llms.txt                  domain-grouped index for LLM consumers
  openapi.json              OpenAPI 3.1 description of the endpoints above

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
SITE_URL = "https://awesomereviewers.com"
API_DOCS_URL = f"{SITE_URL}/api/"
# Name of the site overview under raw/. No instruction may use it as a slug.
SITE_OVERVIEW_SLUG = "site"

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
        "## Developer resources",
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

    if any(entry["slug"] == SITE_OVERVIEW_SLUG for entry in entries):
        raise SystemExit(
            f"an instruction is slugged '{SITE_OVERVIEW_SLUG}', which collides with "
            f"{RAW_DIR}/{SITE_OVERVIEW_SLUG}.md; rename the instruction"
        )
    (RAW_DIR / f"{SITE_OVERVIEW_SLUG}.md").write_text(
        build_site_overview(entries, domains), encoding="utf-8"
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
# single source of truth for the API page, llms.txt and robots.txt, so an
# endpoint cannot be added in one place and forgotten in the others.
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
    return f"{API_DOCS_URL}#error-{code.replace('_', '-')}"


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
            "termsOfService": f"{API_DOCS_URL}#terms",
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
            "description": "Awesome Reviewers API documentation",
            "url": API_DOCS_URL,
        },
        "servers": [{"url": SITE_URL, "description": "Production"}],
        "tags": [
            {"name": "instructions", "description": "Single instructions and domain bundles."},
            {"name": "indexes", "description": "Machine-readable indexes of the whole corpus."},
            {"name": "discovery", "description": "Descriptions of the site itself."},
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
            "openapi": f"{SITE_URL}/openapi.json",
            "resources": DEV_RESOURCES,
            "errors": build_problems(),
        },
    )


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
        f"{SITE_URL}/raw/<slug>.md, and a domain page at /domains/<domain>/ as",
        f"{SITE_URL}/raw/bundles/<domain>.md. Each HTML page links its markdown variant with",
        "<link rel=\"alternate\" type=\"text/markdown\">.",
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
    # The corpus date, not the build date: the description only changes when the
    # thing it describes does.
    version = max(e["updated"] for e in entries)
    write_openapi(entries, domains, version)
    write_api_data(version)


if __name__ == "__main__":
    os.chdir(Path(__file__).resolve().parent)
    main()
