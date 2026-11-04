# Awesome Reviewers

Which checks to run on the code you are writing, and the review prompts for what those checks miss.

**[awesomereviewers.com](https://awesomereviewers.com)**

Two sources of truth, both taken from 256 production open-source repositories:

- **Checks** (`_verifications/`): the linters, type checkers, test runners, scanners and proofs each
  repository runs, found in its CI workflows, pre-commit hooks and task runners, with the commands
  that run them and their documented exit codes.
- **Prompts** (`_reviewers/`): self-contained review instructions (a rule, why it exists, usually an
  example) distilled from recurring reviewer feedback in each repository. They cover what a tool
  cannot decide: design, naming, error semantics, trust boundaries.

## How it works

1. **Changed file → language.** `src/auth/session.py` is Python, `web/app/page.tsx` is TypeScript,
   `.github/workflows/ci.yml` is YAML. The homepage has a box for this; agents use the `extensions`
   map in [`/raw/verify/index.json`](https://awesomereviewers.com/raw/verify/index.json).
2. **Language → playbook.** [`/verify/<language>/`](https://awesomereviewers.com/verify/), also
   published as `/raw/verify/<language>.md`. It has two parts:
   - **Run on every change**: formatting, linting, type checking and tests. Each names the tool most
     scanned repositories in that language run, the share that run it, a command seen in those
     repositories, what its exit codes mean, whether it autofixes, and the alternatives.
   - **Add when the change touches**: one section per kind of change (security, concurrency,
     algorithms, CI config, …), each with the extra checks it calls for and the review prompts for its
     topics, most discussed first.
3. **Run the checks, then apply the prompts.** Checks catch what a tool can find; prompts cover the rest.

## For agents

```bash
# 1. map each changed file to a language
curl -s https://awesomereviewers.com/raw/verify/index.json | jq '.extensions'

# 2. load that language's playbook
curl -s https://awesomereviewers.com/raw/verify/python.md

# 3. fetch the prompts the playbook lists for the kinds of change in the diff
curl -s https://awesomereviewers.com/raw/<slug>.md
```

A playbook is written to be followed as-is:

- Run every check under *Run on every change*. A check marked as autofixing can fix what it finds, so
  run its fix mode first.
- For each section under *Add when the change touches* that describes the diff, run its checks too.
- Read failures with the exit codes the playbook lists (for example, pytest's `5` means no tests were
  collected, not that tests failed).
- Where a check says no tool was detected, no scanned repository in that language runs one the scanner
  recognises. Treat the section's prompts as the verification.
- Apply the listed prompts to the diff.

`/raw/verify/<language>.json` is the same playbook as data, with every candidate tool, its share and
the repositories it was seen in.

## Playbooks

Baseline tools from the current scans. Shares and alternatives are on each page.

| Language | Files | Run on every change |
| --- | --- | --- |
| [Python](https://awesomereviewers.com/verify/python/) | `.py` `.pyi` | `ruff-format`, `ruff-check`, `mypy`, `pytest` |
| [TypeScript](https://awesomereviewers.com/verify/typescript/) | `.ts` `.tsx` `.mts` `.cts` | `prettier`, `eslint`, `tsc`, `vitest` |
| [JavaScript](https://awesomereviewers.com/verify/javascript/) | `.js` `.jsx` `.mjs` `.cjs` | `prettier`, `eslint`, `jest` |
| [Rust](https://awesomereviewers.com/verify/rust/) | `.rs` | `rustfmt`, `clippy`, `cargo-check`, `cargo-test` |
| [Go](https://awesomereviewers.com/verify/go/) | `.go` | `gofmt`, `golangci-lint`, `go-test` (the compiler covers type checking) |
| [YAML and CI workflows](https://awesomereviewers.com/verify/yaml/) | `.yml` `.yaml` | `prettier`; workflow changes add `actionlint` (alternative: `zizmor`) |
| [JSON and TOML](https://awesomereviewers.com/verify/config/) | `.json` `.toml` | `prettier` |
| [Markdown and docs](https://awesomereviewers.com/verify/docs/) | `.md` `.mdx` `.rst` `.txt` | `prettier` |
| Java, Kotlin, Swift, C++, C, C#, Ruby, PHP, Shell, SQL, Dockerfile | see [/verify/](https://awesomereviewers.com/verify/) | cross-language tools and prompts only, for now |

The scanner's tool catalog covers Python, JavaScript, TypeScript, Rust and Go. Playbooks for other
languages still list cross-language checks (CodeQL, Semgrep, gitleaks, codespell, version matrices)
and their prompts.

## What the change touches

The same mapping drives every playbook; each language fills it with its own tools.

| The change touches | Add these checks | Prompt topics |
| --- | --- | --- |
| Any change (baseline) | formatting, linting, type checking, unit and integration tests | Code Style, Naming Conventions |
| Authentication, input handling, secrets, permissions | security scanning, secret scanning, dependency audit | Security |
| Public APIs, signatures, error paths, nullability | type checking, unit and integration tests, property-based tests | API, Error Handling, Null Handling |
| Service and framework code | unit and integration tests, version and platform matrix | Fastify, NestJS, Spring, Axum, Celery, Temporal |
| Algorithms, parsers, data transforms | property-based tests, fuzzing, mutation testing, proofs and specifications | Algorithms |
| Threads, async code, locks, shared state | concurrency model checking, undefined-behaviour detection, property-based tests | Concurrency |
| Network calls, retries, timeouts, protocols | unit and integration tests, fuzzing | Networking, Axios |
| UI components and pages | end-to-end browser tests, linting | React, Next, Next.js, Vue, Angular |
| Databases, migrations, caching | unit and integration tests, version and platform matrix | Database, Migrations, Caching |
| Hot paths and performance | prompts only | Performance Optimization |
| Model, prompt and LLM code | unit and integration tests | AI, Pytorch |
| Logging, metrics, tracing | prompts only | Logging, Observability |
| CI workflows and configuration files | CI workflow linting, file hygiene | CI/CD, Configurations |
| Dependencies and lockfiles | dependency audit, lockfile consistency, version and platform matrix | — |
| The tests themselves | mutation testing, version and platform matrix | Testing |
| Documentation and comments | docs build, spelling | Documentation |

## Verification methods

| Method | Kinds of check |
| --- | --- |
| [Static analysis](https://awesomereviewers.com/methods/static-analysis/) | linting, type checking, security scanning, secret scanning, CI workflow linting, docs build |
| [Testing](https://awesomereviewers.com/methods/testing/) | unit and integration tests, end-to-end browser tests, property-based tests, fuzzing, mutation testing, version and platform matrix |
| [Formatting and hygiene](https://awesomereviewers.com/methods/formatting/) | formatting, file hygiene, spelling |
| [Supply chain](https://awesomereviewers.com/methods/supply-chain/) | dependency audit, lockfile consistency |
| [Formal verification and model checking](https://awesomereviewers.com/methods/formal/) | undefined-behaviour detection, concurrency model checking, proofs and specifications |

Each method page lists the tools behind every kind of check, the languages they cover, how many
scanned repositories run them and a command seen in those repositories. Each source repository has a
page, [`/sources/<owner>-<name>/`](https://awesomereviewers.com/sources/), listing what it runs, linked
to the files each check was found in, and the prompts derived from it.

## Awesome Reviewers API

Everything is a static file. No key, no rate limit, GET only.
Reference: **[awesomereviewers.com/api/](https://awesomereviewers.com/api/)** ·
description: **[/openapi.json](https://awesomereviewers.com/openapi.json)** (OpenAPI 3.1).

```bash
# start here: file extension -> language -> playbook URL
curl https://awesomereviewers.com/raw/verify/index.json

# the checks and prompts for one language
curl https://awesomereviewers.com/raw/verify/python.md

# one prompt
curl https://awesomereviewers.com/raw/<slug>.md

# every prompt in a domain, concatenated
curl https://awesomereviewers.com/raw/bundles/llm-infra.md

# machine index: slug, title, description, domain, topic, language, source, updated, raw URL
curl https://awesomereviewers.com/raw/index.json

# the checks one source repository runs
curl https://awesomereviewers.com/raw/verifications/pallets-flask.json

# domain-grouped listing of the whole corpus
curl https://awesomereviewers.com/llms.txt

# the API surface itself
curl https://awesomereviewers.com/openapi.json
```

| Resource | Path | Type |
| --- | --- | --- |
| OpenAPI description | `/openapi.json` | `application/vnd.oai.openapi+json;version=3.1` |
| API documentation | `/api/` | `text/html` |
| Verification playbooks index | `/raw/verify/index.json` | `application/json` |
| Verification playbook | `/raw/verify/<language>.md` | `text/markdown` |
| Verification playbook (JSON) | `/raw/verify/<language>.json` | `application/json` |
| Corpus index | `/raw/index.json` | `application/json` |
| Single instruction | `/raw/<slug>.md` | `text/markdown` |
| Domain bundle | `/raw/bundles/<domain>.md` | `text/markdown` |
| Verifications index | `/raw/verifications/index.json` | `application/json` |
| Repository verifications | `/raw/verifications/<repository>.json` | `application/json` |
| Source discussions | `/<slug>.json` | `application/json` |
| Search index | `/assets/data/search.json` | `application/json` |
| LLM index | `/llms.txt` | `text/plain` |
| Sitemap | `/sitemap.xml` | `application/xml` |

Every prompt carries the date of the most recent review comment behind it, so a scheduled job can
diff `/raw/index.json` against its last run instead of refetching everything. Each repository scan
carries the commit it was taken at.

An instruction page at `/reviewers/<slug>/` is the same content as `/raw/<slug>.md`, a domain
page at `/domains/<domain>/` as `/raw/bundles/<domain>.md`, and a playbook page at
`/verify/<language>/` as `/raw/verify/<language>.md`; each page links its markdown with
`<link rel="alternate" type="text/markdown">`, and every page links `/openapi.json` as
`rel="service-desc"`. Errors follow [RFC 9457](https://www.rfc-editor.org/rfc/rfc9457) problem
details — see [/api/#errors](https://awesomereviewers.com/api/#errors).

## Prompts by domain

Prompts are also grouped by the kind of system they came from. Each [domain page](https://awesomereviewers.com/domains/)
lists every prompt in it, filterable by topic, language and repository, with the checks its
repositories run most; `/raw/bundles/<domain>.md` has them all in one file.

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
expertise applies to. Topic (`Security`, `Concurrency`, `API`, …) and language cut across domains;
topics are what the playbooks join prompts on.

## Where the data comes from

- **Checks.** bazai's verification scanner reads each repository's default branch: workflow steps,
  pre-commit hooks, Makefile, justfile, tox, nox and package scripts, followed through wrappers such
  as `make lint` or `uv run`, plus config files and manifests. Commands are matched against a catalog
  of known tools, which supplies the method, upstream project, exit codes and autofix. A tool that is
  configured but never run is marked as such. Commands that match no known tool are kept as
  unclassified: shown on repository pages, never recommended.
- **Shares.** A repository counts towards a language when at least a fifth of its prompts are written
  in it, or when it is the repository's most common prompt language. A tool's share is the fraction
  of scanned repositories in that language that run it. Shares say how common a tool is, not how good.
- **Mappings.** What each tool is for, which languages it covers and which checks a kind of change
  calls for are explicit tables in `build_data.py`: `TOOL_PROFILES`, `CHECK_KINDS`, `LANGUAGES` and
  `CHANGES`. Tests require every prompt topic to appear in exactly one `CHANGES` entry and every
  scanned tool to have a profile.
- **Prompts.** Review threads that repeat the same point across a repository are grouped and written
  up as one instruction, with the source threads kept beside it so any prompt can be traced back.

The [How it works](https://awesomereviewers.com/methodology/) page has the details and the known limits.

## Repository layout

```
_reviewers/            source of truth — <slug>.md prompt + <slug>.json source discussions
_verifications/        source of truth — <owner>-<name>.json checks one repository runs
build_data.py          derives everything else from those two directories
_layouts/, _includes/  base, language, method, source, domain and instruction layouts
assets/css/site.scss   the site's only stylesheet
assets/js/site.js      the site's only script
index.html             changed-file finder, languages, change kinds, prompt search
verify.html            playbooks by language    -> /verify/   (one page per language under it)
methods.html           verification methods     -> /methods/  (one page per method under it)
domains.html           prompts by domain        -> /domains/
sources.html           source repositories      -> /sources/  (one page per repository under it)
api.html               API reference            -> /api/
methodology.html       how it works, limits     -> /methodology/
404.html               recovery page, with markdown and problem+json bodies
tests/                 machine-interface tests
edge/                  optional CDN worker for Accept negotiation (not part of the site)
```

Nothing outside `_reviewers/` and `_verifications/` is a source of truth. Playbooks, method and
source pages, domain stats, dates, indexes, raw endpoints, bundles, domain pages, `llms.txt` and
`openapi.json` are all generated and are not committed — see `.gitignore`. What each tool is for,
which languages it covers and which checks a kind of change calls for are explicit tables in
`build_data.py` (`TOOL_PROFILES`, `CHECK_KINDS`, `LANGUAGES`, `CHANGES`); usage shares are counted.

## Local development

```bash
python build_data.py                 # generate derived data (required before the first build)
bundle install
bundle exec jekyll serve
```

`build_data.py` needs only the standard library. Re-run it after changing anything in `_reviewers/`
or `_verifications/`.

```bash
python -m unittest discover -s tests -t .   # scans, playbooks, OpenAPI, llms.txt, 404, discovery links
node --test tests/worker.test.mjs           # the optional edge worker
```

Both suites use only their standard libraries. `pip install openapi-spec-validator` adds a
validation of `openapi.json` against the OpenAPI 3.1 schema to the first suite; without it that one
test skips, so the deploy pipeline never depends on a package index.

## Contributing

- **Fix a prompt:** open a pull request against its file in `_reviewers/`.
- **Fix a domain assignment:** repositories are mapped explicitly in `build_data.py`.
- **Fix a recommendation:** tool profiles and the change-to-check mapping are tables in `build_data.py`;
  a scan is regenerated by bazai's verification scanner, not edited by hand.

## Disclaimer

Community-contributed material derived from public repositories and their review discussions. It is
not official guidance from those projects, a recommended check is what many of them run rather than
an endorsement, and none of it is guaranteed to be correct for your codebase. Report anything harmful
or wrong as an issue.

Maintained by the team at [Baz](https://baz.co). Apache-2.0.
