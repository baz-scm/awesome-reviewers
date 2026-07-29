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

Everything else is derived by `build_data.py` and is **not committed**: `_data/domains.json`,
`_data/entries.json`, `_data/meta.json`, `_data/sources.json`, `assets/data/search.json`,
`domains/*.html`, `raw/**`, `llms.txt`. Re-run `python build_data.py` after touching `_reviewers/`,
and before the first local Jekyll build.

Dates are derived from discussion timestamps, never declared in front matter. Domain is derived from
the source repository via the explicit map in `build_data.py`.

## Site layer

- `_layouts/base.html` — chrome for every page.
- `_layouts/domain.html` — one page per domain, renders all its instructions from `_data/entries.json`.
- `_layouts/reviewer.html` — instruction detail page, metadata from `_data/meta.json[page.slug]`.
- `_includes/row.html` — the one row component shared by the homepage, search results and domain pages.
- `assets/css/site.scss` — the only stylesheet. No webfonts, no CSS framework.
- `assets/js/site.js` — the only script. No dependencies.

## Conventions

- **Copy in place.** Instructions expand inline and copy from wherever they are listed; the detail
  page is for provenance, not for copying.
- **Raw endpoints are part of the product.** `/raw/<slug>.md`, `/raw/bundles/<domain>.md` and
  `/raw/index.json` are the machine interface. Raw markdown files must not carry YAML front matter,
  or Jekyll renders them as pages instead of serving them verbatim.
- **Keep pages light.** `row.html` is rendered thousands of times per domain page; adding markup or
  data attributes there is expensive. Filtering builds its haystack from rendered text at runtime for
  the same reason.
- **Show time.** Anything listing instructions shows when its source discussion was last active, via
  `<time data-date="YYYY-MM-DD">`, which the script turns into a relative label.
- **No marketing copy.** Describe what something is and what it does.

## Watch out for

- Do not add `include: _reviewers` back to `_config.yml`: the discussion JSON is already copied to
  `/<slug>.json` as collection static files, and the include duplicates 157 MB.
- `github-pages` pulls in `jekyll-github-metadata`, which calls the GitHub API at build time. Where
  that is blocked, build with `JEKYLL_NO_BUNDLER_REQUIRE=true`.
- A full build renders 5k+ pages and takes about a minute; expect that locally and in CI.
