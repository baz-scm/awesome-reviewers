# Awesome Reviewers

Expert engineering instructions for AI and infrastructure domains, distilled from code review
discussions in production open-source repositories.

**[awesomereviewers.com](https://awesomereviewers.com)**

Each entry is a self-contained instruction — a rule, why it exists, and usually an example — written
from recurring reviewer feedback in one repository. They are plain markdown, so they drop into an
agent, a review harness, a context broker, or a prompt you are assembling by hand.

## Awesome Reviewers API

Everything is a static file. No key, no authentication, GET only.
Start here: **[awesomereviewers.com/developers/](https://awesomereviewers.com/developers/)** ·
reference: **[/api/](https://awesomereviewers.com/api/)** ·
description: **[/openapi.json](https://awesomereviewers.com/openapi.json)** (OpenAPI 3.1) ·
agents: **[/agents.md](https://awesomereviewers.com/agents.md)**.

```bash
# what this interface is, and what may change
curl https://awesomereviewers.com/v1/version.json

# the index: every instruction, with its markdown and JSON URLs
curl https://awesomereviewers.com/v1/index.json

# one instruction as typed JSON, body included
curl https://awesomereviewers.com/v1/instructions/<slug>.json

# one instruction as markdown, to paste into a prompt
curl https://awesomereviewers.com/raw/<slug>.md

# every instruction in a domain, concatenated
curl https://awesomereviewers.com/raw/bundles/llm-infra.md

# domain-grouped listing of the whole corpus
curl https://awesomereviewers.com/llms.txt
```

| Resource | Path | Type |
| --- | --- | --- |
| OpenAPI description | `/openapi.json` | `application/vnd.oai.openapi+json;version=3.1` |
| API documentation | `/api/` | `text/html` |
| Developer portal | `/developers/` | `text/html` |
| Agent instructions | `/agents.md` | `text/markdown` |
| API catalogue | `/.well-known/api-catalog` | `application/linkset+json` |
| Interface version and policies | `/v1/version.json` | `application/json` |
| Corpus index (v1) | `/v1/index.json` | `application/json` |
| Domains (v1) | `/v1/domains.json` | `application/json` |
| Facets: topics, languages, repositories | `/v1/facets.json` | `application/json` |
| Source repositories (v1) | `/v1/sources.json` | `application/json` |
| Single instruction (v1) | `/v1/instructions/<slug>.json` | `application/json` |
| Error catalogue / one error | `/v1/errors/index.json`, `/v1/errors/<code>.json` | `application/json` |
| Corpus index | `/raw/index.json` | `application/json` |
| Single instruction | `/raw/<slug>.md` | `text/markdown` |
| Domain bundle | `/raw/bundles/<domain>.md` | `text/markdown` |
| Source discussions | `/<slug>.json` | `application/json` |
| Search index | `/assets/data/search.json` | `application/json` |
| LLM index | `/llms.txt` | `text/plain` |
| Sitemap | `/sitemap.xml` | `application/xml` |
| Recovery body | `/404.md` | `text/markdown` |
| CLI | `/cli/awesome-reviewers.py` | `text/x-python` |

Every instruction carries the date of the most recent review comment behind it, so a scheduled job
can diff `/v1/index.json` against its last run instead of refetching everything.

**Versioning.** The interface is versioned in the URL path: `/v1/**` keeps its response shapes and a
breaking change ships as `/v2/**` beside it. The unversioned paths (`/raw/**`, `/llms.txt`) predate
the prefix and are maintained as aliases of the v1 shapes. A retiring endpoint answers with
`Deprecation` ([RFC 9745](https://www.rfc-editor.org/rfc/rfc9745)), `Sunset`
([RFC 8594](https://www.rfc-editor.org/rfc/rfc8594)) at least 180 days later, and a `Link` with
`rel="deprecation"`; live deprecations are listed in `/v1/version.json`.

**Pacing.** The static origin does not throttle. Where the optional [`edge/`](edge/) worker is
deployed, the quota is 600 requests per 60 seconds per client IP, advertised in `RateLimit-Policy`
and `RateLimit`, with `Retry-After` on a 429.

**Representations.** An instruction page at `/reviewers/<slug>/` is the same content as
`/raw/<slug>.md` and `/v1/instructions/<slug>.json`; a domain page at `/domains/<domain>/` as
`/raw/bundles/<domain>.md`; `/developers/`, `/about/`, `/contact/` and `/privacy/` as
`/raw/<page>.md`. Each page links its alternates with `<link rel="alternate">`, and every page links
`/openapi.json` (`rel="service-desc"`), `/v1/version.json` (`rel="service-meta"`),
`/.well-known/api-catalog` (`rel="api-catalog"`) and `/agents.md` (`rel="help"`). Errors follow
[RFC 9457](https://www.rfc-editor.org/rfc/rfc9457) problem details — see
[/api/#errors](https://awesomereviewers.com/api/#errors).

## CLI

```bash
curl -sSO https://awesomereviewers.com/cli/awesome-reviewers.py
chmod +x awesome-reviewers.py

./awesome-reviewers.py domains
./awesome-reviewers.py search "kv cache" --limit 5
./awesome-reviewers.py get <slug> --json
./awesome-reviewers.py bundle llm-infra -o rubric.md
./awesome-reviewers.py sync ./corpus --domain security
```

One file, standard library only, Python 3.9+. `sync` fetches only what changed since the last run.
It is not published to a package registry yet, so there is nothing to `pip install`.

## Domains

| Domain | What it covers |
| --- | --- |
| `ai-agents` | Agent loops, tool calling, prompt and context assembly, agent SDKs, coding assistants |
| `llm-infra` | Inference servers, model gateways and routers, KV caching, retrieval and ingestion |
| `ml-systems` | Training and inference frameworks, tensor and kernel code, ML platforms |
| `orchestration` | Kubernetes, schedulers, service meshes, container tooling, workflow engines |
| `cloud-infra` | Infrastructure as code, cloud SDKs, edge runtimes, proxies, gateways, tunnels |
| `data-systems` | Query engines, storage, replication, streaming, ORMs, analytics backends |
| `observability` | Metrics, tracing, logging, error tracking, instrumentation |
| `security` | Static analysis, cloud posture scanning, auth, authorization, secrets |
| `runtimes` | Interpreters, compilers, async runtimes, parsers, low-level systems code |
| `devtools` | Editors, terminals, build systems, package managers, linters, test runners |
| `app-frameworks` | Web and mobile frameworks, component libraries, API layers, product code |
| `docs` | Reference material and learning resources — mostly writing and structure guidance |

Domain is assigned from the source repository, because that determines what kind of system the
expertise applies to. Topic (`Security`, `Concurrency`, `API`, …) and language cut across domains and
are filterable on every domain page.

## Repository layout

```
_reviewers/            source of truth — <slug>.md instruction + <slug>.json source discussions
build_data.py          derives everything else from _reviewers/
_layouts/, _includes/  base, page, domain and instruction layouts
assets/css/site.scss   the site's only stylesheet
assets/js/site.js      the site's only script
index.html             search, domains, recently updated, JSON-LD identity
domains.html           domain overview          -> /domains/
sources.html           source repositories      -> /sources/
api.html               API reference            -> /api/
methodology.html       how entries are derived  -> /methodology/
developers.md          developer portal         -> /developers/  (+ /raw/developers.md)
about.md               what this is             -> /about/       (+ /raw/about.md)
contact.md             where to reach us        -> /contact/     (+ /raw/contact.md)
privacy.md             what runs, what is kept  -> /privacy/     (+ /raw/privacy.md)
404.html               recovery page, with markdown and problem+json bodies
cli/                   the published single-file CLI
tests/                 machine-interface and CLI tests
edge/                  optional CDN worker for negotiation, quotas and deprecation headers
```

Prose pages are authored as markdown so `build_data.py` can publish the same text verbatim at
`/raw/<page>.md`; the wrapper markup lives in `_layouts/page.html`, and the build fails if one of
them contains Liquid that the twin would leak unrendered.

Nothing outside `_reviewers/` is a source of truth. Domain stats, dates, indexes, raw endpoints,
bundles, domain pages, `llms.txt`, `agents.md`, `404.md`, `openapi.json`, `v1/**` and
`.well-known/api-catalog` are all generated and are not committed — see `.gitignore`.

## Local development

```bash
python build_data.py                 # generate derived data (required before the first build)
bundle install
bundle exec jekyll serve
```

`build_data.py` needs only the standard library. Re-run it after changing anything in `_reviewers/`.

```bash
python -m unittest discover -s tests -t .   # OpenAPI, /v1, errors, llms.txt, agents.md, 404,
                                            # trust pages, JSON-LD, discovery links, CLI
node --test tests/worker.test.mjs           # the optional edge worker
```

Both suites use only their standard libraries. `pip install openapi-spec-validator` adds a
validation of `openapi.json` against the OpenAPI 3.1 schema to the first suite; without it that one
test skips, so the deploy pipeline never depends on a package index.

## Contributing

- **Add a repository:** submit it from the [homepage](https://awesomereviewers.com/) and
  it is queued for extraction. Private repositories go through [Baz](https://baz.co/agents).
- **Fix an instruction:** open a pull request against its file in `_reviewers/`.
- **Fix a domain assignment:** repositories are mapped explicitly in `build_data.py`.

## Disclaimer

Community-contributed material distilled from public review discussions. It is not official guidance
from the projects it was derived from, and it is not guaranteed to be correct for your codebase.
Report anything harmful or wrong as an issue.

Maintained by the team at [Baz](https://baz.co). Apache-2.0.
