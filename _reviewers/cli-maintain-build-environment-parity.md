---
title: maintain build environment parity
description: Ensure that local development and CI/CD environments use identical build
  commands and dependency management strategies to prevent deployment issues and environment
  drift. When introducing local-specific build targets, consider whether the same
  approach should be adopted in CI pipelines to maintain consistency.
repository: snyk/cli
label: CI/CD
language: Other
comments_count: 2
repository_stars: 5178
---

Ensure that local development and CI/CD environments use identical build commands and dependency management strategies to prevent deployment issues and environment drift. When introducing local-specific build targets, consider whether the same approach should be adopted in CI pipelines to maintain consistency.

Avoid creating separate build paths that could diverge over time. Instead of having different commands like `build` vs `build-local`, standardize on a single approach that works across all environments.

For dependency management, be consistent about when to use clean installs vs incremental installs:

```makefile
# Instead of different targets:
build-local: pre-build
	source .venv/bin/activate; make build-full

# Prefer unified approach:
build: pre-build
	@if [ -f .venv/bin/activate ]; then source .venv/bin/activate; fi
	make build-full
```

When optimizing for performance (like using `npm i` instead of `npm ci`), ensure the optimization logic is consistent between local and CI environments, or clearly document why they differ.