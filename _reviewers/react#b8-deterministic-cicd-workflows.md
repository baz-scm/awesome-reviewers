---
title: Deterministic CI/CD Workflows
description: 'Design CI/CD workflows so they are deterministic, stable, and safe:


  - For browser- or runtime-dependent tests, do not rely on whatever Chrome happens
  to be present in GitHub-hosted images. Use the browser version that your test framework
  (e.g., Playwright) installs/ships, so all runs share the same tooling.'
repository: facebook/react#b8
label: CI/CD
language: Yaml
comments_count: 2
repository_stars: 251889
---

Design CI/CD workflows so they are deterministic, stable, and safe:

- For browser- or runtime-dependent tests, do not rely on whatever Chrome happens to be present in GitHub-hosted images. Use the browser version that your test framework (e.g., Playwright) installs/ships, so all runs share the same tooling.
- For publishing, require a protected environment and least-privilege permissions (OIDC-based trusted publishing rather than user secrets). Add explicit version safety checks (e.g., refuse placeholder versions) and preflight behavior so you don’t accidentally publish incorrect releases.

Example patterns (adapt as needed):
```yaml
# Browser stability: rely on Playwright-managed Chromium/Chrome rather than base image
- name: Run Playwright tests
  run: yarn test:e2e
  # (Ensure your test command uses Playwright’s browser, not /usr/bin/google-chrome from the runner.)

# Publish safety: protected environment + OIDC + pinned checkout
jobs:
  publish:
    environment: npm
    permissions:
      id-token: write
      contents: read
    steps:
      - uses: actions/checkout@v4
        with:
          ref: ${{ github.sha }}
      # Refuse placeholder versions before publishing
      - run: |
          version="$(node -p "require('./package.json').version")"
          if [ "$version" = "0.0.0" ]; then
            echo "Refusing to publish placeholder version 0.0.0" >&2
            exit 1
          fi
      - run: yarn publish
```

Apply this standard anytime you see CI steps that depend on external binaries/versions (browsers, system tools) or automated deployments/releases.