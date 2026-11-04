# Awesome Reviewers — repository guidelines

## What this project is

A directory of review and verification techniques, browsable in one place. Two kinds of first-party
entry: **reviewers** (instructions distilled from real code review discussions) and **verification**
techniques (how to build a check and how to recognise it in a repository). Modelled on skills.sh:
one list, search, a few filters, one page per entry.

It is a Jekyll site on GitHub Pages. Static, no build step beyond Jekyll, no runtime dependencies.

## Source of truth

- `_reviewers/<slug>.md` — front matter (`title`, `description`, `repository`, `label`, `language`,
  `comments_count`, `repository_stars`) plus the instruction body. Every value is rendered as written.
- `_reviewers/<slug>.json` — the discussions the instruction was derived from. Provenance only; excluded
  from the site output.
- `_verification/<slug>.md` — front matter (`title`, `id`, `tactic`, `description`, `subtechniques`,
  `packages`, `craft`, `reverse`). `id` is `V####`, sub-technique ids are `V####.###`.

Nothing else is derived or committed. Dates, counts and filter values come from the front matter.

## Site layer

- `index.html` — the directory: hero, search, type tabs, category/language/sort filters, one ranked list.
- `_includes/row.html` — the one row component. Keep its `data-*` attributes to what filtering needs.
- `_layouts/reviewer.html` — one reviewer page: instruction with copy button, metadata.
- `_layouts/technique.html` — one verification page: sub-techniques, how to build it, signals, packages.
- `assets/js/site.js` — filters and sorts the rendered rows; reads and writes the query string.
- `assets/css/site.scss` — the only stylesheet. Colours are tokens on `:root`, with dark mode.

## Conventions

- **Escape author text.** Jekyll does not HTML-escape Liquid output. Every front-matter value printed in a
  layout or include goes through `| escape`; a `<` in a title otherwise corrupts the list.
- **Keep the list light.** It renders every entry so search works without a server. Do not add markup or
  data attributes per row without a reason.
- **No marketing copy.** Describe what an entry is and what it does.

## Validation

`python -m unittest discover -s tests -t .` checks front matter in both collections: required fields,
integer counts, unique technique ids, sub-technique ids under their parent. CI runs it before
`jekyll build`. Jekyll itself fails the build on bad YAML.

## Watch out for

- Do not add `include: _reviewers` to `_config.yml`: the discussion JSON is excluded on purpose.
- Local builds need a UTF-8 locale (`LANG=C.UTF-8`) or the Sass step fails on a theme file.
- `github-pages` calls the GitHub API at build time; where that is blocked, build with
  `JEKYLL_NO_BUNDLER_REQUIRE=true`.
