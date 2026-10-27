---
title: Deterministic, Safe CI/CD
description: Ensure CI/CD workflows are deterministic and release-safe by (1) not
  depending on unstable runner environment details, and (2) keeping publish guardrails
  intentional and minimal.
repository: facebook/react#b15
label: CI/CD
language: Yaml
comments_count: 2
repository_stars: 251891
---

Ensure CI/CD workflows are deterministic and release-safe by (1) not depending on unstable runner environment details, and (2) keeping publish guardrails intentional and minimal.

Apply these rules:
- Pin or reuse the exact runtime dependencies your tooling uses. For browser-based tests, prefer Playwright’s bundled/selected browser over whatever Chrome happens to exist on the GitHub runner.
- Avoid “environment drift” checks that still depend on runner-provided versions. Instead, derive the browser version from the pinned Playwright configuration/artifacts.
- For release/publish workflows, add explicit checks that prevent obviously invalid releases (e.g., placeholder versions). For validations already guaranteed by `npm publish`, don’t duplicate them unless you gain meaningful CI-time value.

Example pattern (browser version alignment in E2E):
```yaml
- name: Run Playwright E2E
  run: |
    # Don’t use /usr/bin/google-chrome --version from the base image.
    # Use the Playwright-installed browser that matches your pinned Playwright version.
    yarn test:e2e
```

Example pattern (release guardrail, not duplication):
```bash
version="$(node -p "require('./package.json').version")"
if [ "$version" = "0.0.0" ]; then
  echo "Refusing to publish placeholder version 0.0.0" >&2
  exit 1
fi
# Rely on npm publish for already-published version handling.
# Only add extra checks when they materially improve workflow behavior.
```