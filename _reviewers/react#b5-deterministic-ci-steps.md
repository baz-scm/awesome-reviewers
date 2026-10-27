---
title: Deterministic CI Steps
description: 'Ensure CI workflows are deterministic and their failure signals are
  predictable.


  1) Pin/deduce runtime versions from the test framework

  - Don’t rely on mutable GitHub runner defaults for critical tools (e.g., Chrome/Chromium).'
repository: facebook/react#b5
label: CI/CD
language: Yaml
comments_count: 2
repository_stars: 251886
---

Ensure CI workflows are deterministic and their failure signals are predictable.

1) Pin/deduce runtime versions from the test framework
- Don’t rely on mutable GitHub runner defaults for critical tools (e.g., Chrome/Chromium).
- Prefer using the browser version packaged/selected by your test framework (e.g., Playwright) or lock the Chrome version explicitly.

2) Treat shell snippets and log strings as code
- Quote/escape characters (notably backticks) so CI output is literal and won’t be interpreted unexpectedly.

Example (YAML/bash style):
```yml
- name: Check Chrome version (use the Playwright-aligned browser)
  run: |
    # Prefer deriving the browser version from the same Playwright package/version
    /usr/bin/google-chrome --version

- name: Fail with correct literal instructions
  run: |
    git diff --exit-code || (
      echo "There was a change to the generated artifact. Run \`yarn generate-inline-fizz-runtime\` and check in the result." 
      && false
    )
```

Apply this standard when adding new CI jobs, especially ones that execute browser-based or code-generation steps, to avoid flaky runs and misleading failure output.