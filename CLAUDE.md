# Awesome Reviewers — repository guidelines

## What this project is

A library of expert engineering instructions for AI and infrastructure domains, distilled from code
review discussions in production open-source repositories. Consumers are people and agents that need
raw, copy-ready expertise: agents, review harnesses, context brokers.

It is a Jekyll site on GitHub Pages. Keep it that way — static, dependency-light, no build step
beyond Jekyll and one Python script.

## Source of truth

`_reviewers/` only:

- `<slug>.md` — front matter (`title`, `description`, `repository`, `label`, `language`,
  `comments_count`, `repository_stars`) plus the instruction body in markdown.
- `<slug>.json` — the review discussions the instruction was derived from.

Everything else is derived by `build_data.py` and is **not committed**: `_data/api.json`,
`_data/domains.json`, `_data/entries.json`, `_data/meta.json`, `_data/sources.json`,
`assets/data/search.json`, `domains/*.html`, `raw/**`, `llms.txt`, `agents.md`, `404.md`,
`openapi.json`, `v1/**`, `.well-known/api-catalog`. Re-run `python build_data.py` after touching
`_reviewers/`, and before the first local Jekyll build.

Dates are derived from discussion timestamps, never declared in front matter. Domain is derived from
the source repository via the explicit map in `build_data.py`.

## Site layer

- `_layouts/base.html` — chrome for every page, plus the discovery `<link>`s.
- `_layouts/page.html` — chrome for the markdown-authored prose pages.
- `_layouts/domain.html` — one page per domain, renders all its instructions from `_data/entries.json`.
- `_layouts/reviewer.html` — instruction detail page, metadata from `_data/meta.json[page.slug]`.
- `_includes/row.html` — the one row component shared by the homepage, search results and domain pages.
- `assets/css/site.scss` — the only stylesheet. No webfonts, no CSS framework.
- `assets/js/site.js` — the only script. No dependencies.
- Prose pages (`PROSE_PAGES` in `build_data.py`: developers, about, contact, privacy) are markdown
  with `layout: page`, published verbatim at `/raw/<page>.md`. Keep markup and Liquid out of them —
  the build fails on Liquid, because the twin would leak it unrendered.

## Machine interface

- `openapi.json` (OpenAPI 3.1), the `/api/` page, `/developers/`, `llms.txt`, `agents.md`,
  `robots.txt`, `/v1/version.json` and `README.md` all describe the same endpoints. `DEV_RESOURCES`
  in `build_data.py` is the single source of truth; add an endpoint there rather than in seven
  places, and the tests fail if one of them drifts.
- `/v1/**` is the versioned JSON surface: response shapes are stable there, and a breaking change
  ships as `/v2/**` beside it. `API_VERSION`, `VERSION_POLICY` and `DEPRECATIONS` in `build_data.py`
  define the policy; `/v1/version.json` publishes it. `DEPRECATIONS` there and in `edge/worker.js`
  have to move together.
- `RATE_LIMIT_*` in `build_data.py` and `RATE_LIMIT` in `edge/worker.js` are the same quota, stated
  in the syntax of the RateLimit header fields. The origin does not throttle; say so rather than
  implying a limit that is not applied.
- Errors follow RFC 9457 problem details. `PROBLEM_TYPES` in `build_data.py` defines them; every
  `type` URI must resolve to an `#error-<code>` anchor on the `/api/` page, and each one is also
  published as a document under `/v1/errors/`.
- `404.html` is what GitHub Pages serves for every missing path. It renders
  `build_not_found_markdown()` — the same text as `/404.md` and the same the worker returns to a
  markdown client — plus the problem details in a `<script type="application/problem+json">`,
  because a static host cannot return a JSON body with a 404 status.
- `/.well-known/api-catalog` is RFC 9727 in the RFC 9264 linkset format, which needs
  `include: [.well-known]` in `_config.yml` because Jekyll skips dot-directories.
- JSON-LD identity lives on the homepage (`WebSite`, `Organization`, `Dataset`, `WebAPI`) and the
  `/api/` page. Keep the counts Liquid-derived so they cannot go stale.
- `cli/awesome-reviewers.py` is served at `/cli/awesome-reviewers.py` and is part of the interface:
  standard library only, and every URL it builds is asserted against `build_data.py` in the tests.
- `edge/` is an optional CDN worker that adds `Accept` negotiation, real JSON and markdown errors,
  the RateLimit and Deprecation headers and the catalogue media type. It is excluded from the Jekyll
  build and the site does not depend on it.
- Tests: `python -m unittest discover -s tests -t .` and `node --test tests/worker.test.mjs`. Both
  run in CI before `jekyll build`.

## Conventions

- **Copy in place.** Instructions expand inline and copy from wherever they are listed; the detail
  page is for provenance, not for copying.
- **Raw endpoints are part of the product.** `/raw/<slug>.md`, `/raw/bundles/<domain>.md`,
  `/raw/index.json`, `/v1/**`, `agents.md` and `404.md` are the machine interface. Generated
  markdown must not carry YAML front matter, or Jekyll renders it as a page instead of serving it
  verbatim.
- **Say what is actually true of the origin.** Where a behaviour needs the edge worker (`Accept`
  negotiation, JSON errors, enforced quotas), document it as that and keep the static-origin
  behaviour described too. Never describe a media type or header the origin cannot produce as if it
  could.
- **Keep pages light.** `row.html` is rendered thousands of times per domain page; adding markup or
  data attributes there is expensive. Filtering builds its haystack from rendered text at runtime for
  the same reason.
- **Show time.** Anything listing instructions shows when its source discussion was last active, via
  `<time data-date="YYYY-MM-DD">`, which the script turns into a relative label.
- **No marketing copy.** Describe what something is and what it does.

## Watch out for

- Do not add `include: _reviewers` back to `_config.yml`: the discussion JSON is already copied to
  `/<slug>.json` as collection static files, and the include duplicates 157 MB. The one include the
  site does need is `.well-known`.
- `v1/instructions/` is one JSON document per instruction — 5k files, ~26 MB. That is the price of a
  typed representation with the body in it; keep an eye on the total if another per-instruction
  artifact is proposed.
- A prose page slug cannot collide with an instruction slug (`RESERVED_SLUGS`); the build stops if
  one does.
- `github-pages` pulls in `jekyll-github-metadata`, which calls the GitHub API at build time. Where
  that is blocked, build with `JEKYLL_NO_BUNDLER_REQUIRE=true`.
- A full build renders 5k+ pages and takes about a minute; expect that locally and in CI.
