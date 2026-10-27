---
title: Deterministic CI Practices
description: 'CI pipelines should be deterministic: use the same pinned/derived runtime
  versions your tooling expects (especially browsers for e2e) and ensure CI shell
  commands/messages don’t accidentally execute due to quoting/escaping issues.'
repository: facebook/react#b10
label: CI/CD
language: Yaml
comments_count: 2
repository_stars: 251894
---

CI pipelines should be deterministic: use the same pinned/derived runtime versions your tooling expects (especially browsers for e2e) and ensure CI shell commands/messages don’t accidentally execute due to quoting/escaping issues.

Apply this:
- Version consistency for e2e: prefer the browser version that Playwright downloads/uses (or reuse its archived Chromium). If reusing isn’t feasible, explicitly lock the Chrome/Chromium version so CI doesn’t drift.
- Safe shell semantics: when writing CI steps that fail with guidance, escape shell-sensitive characters (notably backticks) so the shell treats them as literals.

Example pattern (safe failure message):
```sh
# In a CI step
yarn generate-inline-fizz-runtime
git diff --exit-code \
  || (echo "There was a change to the Fizz runtime. Run \`yarn generate-inline-fizz-runtime\` and check in the result." && false)
```

Example pattern (browser version consistency):
- In your workflow, derive the Chrome/Chromium version from Playwright’s installed binaries/archive rather than relying on the runner image’s Chrome, and lock it across all CI runs.