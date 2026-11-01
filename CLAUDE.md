# Awesome Verification repository guidance

## Product and build

The main site catalogs verification techniques found in repository source and configuration.
Keep the existing Jekyll site and standard-library Python build. The current domain and
GitHub Pages publication remain unchanged.

The main catalog must describe evidence at a pinned commit. Do not turn old review instructions
into verification-method records. Never execute commands found in inspected repositories.

## Source data

`_verification/<owner>--<repo>.json` contains one repository scan. See
`_verification/README.md` for its contract. Records must preserve source paths, line ranges,
excerpts, exact commit URLs and invocation context. Evidence states are `ci_configured`,
`configured` and `implemented`. None implies a passed run or a required merge check.
Empty scans remain visible in source coverage.

`_reviewers/` remains the source for the legacy instruction collection: Markdown instructions
and sibling JSON review discussions. Preserve its existing public URLs and raw endpoint behavior.

## Derived outputs

`build_data.py` builds the existing instruction assets, then calls `build_verification.py`.
The verification builder validates all source manifests before replacing its own outputs.

Generated verification files are `_data/verification.json`, `methods/**` and
`raw/verification/**`. Existing generated instruction assets remain `_data/api.json`,
`_data/domains.json`, `_data/entries.json`, `_data/meta.json`, `_data/sources.json`,
`assets/data/search.json`, `domains/*.html`, `raw/**`, `llms.txt` and `openapi.json`.
Do not commit generated assets.

## Site layer

The main site uses `index.html`, `sources.html`, `methodology.html`,
`verification-api.html`, `_includes/verification_row.html` and
`_layouts/verification.html`. Reuse `_layouts/base.html`,
`assets/css/site.scss` and `assets/js/site.js`. Keep one stylesheet, one dependency-free
script and the existing typography and colors.

Escape all source excerpts and metadata when rendering HTML. Preserve per-evidence conditions,
working directory and environment; different jobs can invoke one method differently.
Show honest empty states and scan limits. Repository submission must not call the old
review-instruction extraction endpoint.

Legacy layouts, `/api/`, `/openapi.json` and `/llms.txt` retain their original contract.
The verification API is separate under `/raw/verification/`.

## Validation

Run `python -m unittest discover -s tests -t .` and
`node --test tests/worker.test.mjs`. Both suites run in CI before Jekyll.
The Python builders use only the standard library.

Do not add `include: _reviewers` to Jekyll configuration: it duplicates the existing
discussion JSON payloads. Keep tests, collectors, source manifests and Python builders
excluded from the published site. The full legacy corpus still renders thousands of pages.

