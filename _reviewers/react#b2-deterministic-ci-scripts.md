---
title: Deterministic CI Scripts
description: 'CI workflows should be deterministic and safe: (1) pin/reuse runtime
  dependencies (especially browsers) to the exact versions your test tooling provides,
  and (2) ensure workflow shell commands don’t accidentally execute shell syntax.'
repository: facebook/react#b2
label: CI/CD
language: Yaml
comments_count: 2
repository_stars: 251882
---

CI workflows should be deterministic and safe: (1) pin/reuse runtime dependencies (especially browsers) to the exact versions your test tooling provides, and (2) ensure workflow shell commands don’t accidentally execute shell syntax.

Apply this by:
- Use the browser version that Playwright bundles (or otherwise lock/derive Chrome/Chromium from the same source) instead of relying on GitHub image defaults.
- In workflow `run:` scripts, escape shell-special characters in messages/logs so they render literally.

Example (safe failure message in a workflow):
```sh
yarn generate-inline-fizz-runtime
# Ensure backticks don’t trigger command substitution
git diff --exit-code || (
  echo "There was a change to the Fizz runtime. Run \`yarn generate-inline-fizz-runtime\` and check in the result." && false
)
```

Example (browser version consistency):
- Configure your e2e job to use the same Chromium/Chrome version Playwright downloads (or reuse the Playwright archive) rather than calling `/usr/bin/google-chrome --version` from the base image.