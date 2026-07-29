# Awesome Reviewers

Expert engineering instructions for AI and infrastructure domains, distilled from code review
discussions in production open-source repositories.

**[awesomereviewers.com](https://awesomereviewers.com)**

Each entry is a self-contained instruction — a rule, why it exists, and usually an example — written
from recurring reviewer feedback in one repository. They are plain markdown, so they drop into an
agent, a review harness, a context broker, or a prompt you are assembling by hand.

## Raw access

Everything is a static file. No key, no rate limit.

```bash
# one instruction
curl https://awesomereviewers.com/raw/<slug>.md

# every instruction in a domain, concatenated
curl https://awesomereviewers.com/raw/bundles/llm-infra.md

# machine index: slug, title, description, domain, topic, language, source, updated, raw URL
curl https://awesomereviewers.com/raw/index.json

# domain-grouped listing of the whole corpus
curl https://awesomereviewers.com/llms.txt
```

Every instruction carries the date of the most recent review comment behind it, so a scheduled job
can diff `/raw/index.json` against its last run instead of refetching everything.

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
_layouts/, _includes/  base, domain and instruction layouts
assets/css/site.scss   the site's only stylesheet
assets/js/site.js      the site's only script
index.html             search, domains, recently updated
domains.html           domain overview          -> /domains/
sources.html           source repositories      -> /sources/
api.html               raw endpoint reference   -> /api/
methodology.html       how entries are derived  -> /methodology/
```

Nothing outside `_reviewers/` is a source of truth. Domain stats, dates, indexes, raw endpoints,
bundles, domain pages and `llms.txt` are all generated and are not committed — see `.gitignore`.

## Local development

```bash
python build_data.py                 # generate derived data (required before the first build)
bundle install
bundle exec jekyll serve
```

`build_data.py` needs only the standard library. Re-run it after changing anything in `_reviewers/`.

## Contributing

- **Add a repository:** submit it from the [sources page](https://awesomereviewers.com/sources/) and
  it is queued for extraction. Private repositories go through [Baz](https://baz.co/agents).
- **Fix an instruction:** open a pull request against its file in `_reviewers/`.
- **Fix a domain assignment:** repositories are mapped explicitly in `build_data.py`.

## Disclaimer

Community-contributed material distilled from public review discussions. It is not official guidance
from the projects it was derived from, and it is not guaranteed to be correct for your codebase.
Report anything harmful or wrong as an issue.

Maintained by the team at [Baz](https://baz.co). Apache-2.0.
