---
title: Deterministic CI Tooling
description: 'Ensure CI workflows are deterministic and that command strings behave
  exactly as intended.


  Apply two rules:

  1) **Pin/align external tooling versions to test framework artifacts** (don’t rely
  on mutable runner defaults like preinstalled Chrome). For browser-based E2E tests,
  use the Chrome/Chromium version that your Playwright version uses, or reuse the...'
repository: facebook/react#b6
label: CI/CD
language: Yaml
comments_count: 2
repository_stars: 251888
---

Ensure CI workflows are deterministic and that command strings behave exactly as intended.

Apply two rules:
1) **Pin/align external tooling versions to test framework artifacts** (don’t rely on mutable runner defaults like preinstalled Chrome). For browser-based E2E tests, use the Chrome/Chromium version that your Playwright version uses, or reuse the Playwright-provided binaries (with any required bootstrapping), so all CI runs test the same browser.

2) **Quote/escape CI command text correctly** so guidance strings are literal and never accidentally executed.

Example pattern (escaping literals in CI output):
```yaml
- run: |
    yarn generate-inline-fizz-runtime
    git diff --exit-code || (
      echo "There was a change to the Fizz runtime. Run \`yarn generate-inline-fizz-runtime\` and check in the result." && false
    )
```

Example pattern (pin browser version in CI):
- Don’t run `google-chrome --version` and proceed assuming it’s stable on the runner.
- Instead, derive the Chrome/Chromium version from your Playwright setup (or archive) and use that consistently across all E2E jobs.