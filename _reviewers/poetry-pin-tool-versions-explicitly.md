---
title: Pin tool versions explicitly
description: Always specify exact versions for tools and dependencies in CI/CD workflows
  to ensure reproducible builds and avoid issues with cached or default system versions.
  Use package managers and version pinning rather than relying on system-installed
  tools.
repository: python-poetry/poetry
label: CI/CD
language: Yaml
comments_count: 2
repository_stars: 33496
---

Always specify exact versions for tools and dependencies in CI/CD workflows to ensure reproducible builds and avoid issues with cached or default system versions. Use package managers and version pinning rather than relying on system-installed tools.

When possible, prefer managed binaries over system defaults. For example, use npm-managed tools via npx, and pin Python versions to specific releases rather than using generic version specifiers.

Example:
```yaml
# Instead of:
- run: hugo --minify --logLevel info
python-version: ["3.6", "3.7", "3.8", "3.9", "pypy-3.7"]

# Use:
- run: npx hugo --minify --logLevel info  
python-version: ["3.6", "3.7", "3.8", "3.9", "pypy-3.7-v7.3.7"]
```

This practice prevents build failures caused by version mismatches, ensures consistent behavior across different runner environments, and takes advantage of bug fixes in newer tool versions.