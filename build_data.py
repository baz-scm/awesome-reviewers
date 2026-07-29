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
SITE_URL = "https://awesomereviewers.com"

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


def write_raw(entries: list[dict], domains: list[dict]) -> None:
    if RAW_DIR.exists():
        shutil.rmtree(RAW_DIR)
    (RAW_DIR / "bundles").mkdir(parents=True)

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


def write_llms(entries: list[dict], domains: list[dict]) -> None:
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
        "## Endpoints",
        "",
        f"- Machine index: {SITE_URL}/raw/index.json",
        f"- Single instruction: {SITE_URL}/raw/<slug>.md",
        f"- Whole domain: {SITE_URL}/raw/bundles/<domain>.md",
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

    LLMS_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
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


if __name__ == "__main__":
    os.chdir(Path(__file__).resolve().parent)
    main()
