---
title: explicit CI/CD configuration
description: Always use explicit configuration in CI/CD workflows rather than relying
  on defaults or convenience shortcuts. This includes pinning exact tool versions,
  specifying action parameters explicitly, and choosing reliable installation methods.
repository: gofiber/fiber
label: CI/CD
language: Yaml
comments_count: 3
repository_stars: 37560
---

Always use explicit configuration in CI/CD workflows rather than relying on defaults or convenience shortcuts. This includes pinning exact tool versions, specifying action parameters explicitly, and choosing reliable installation methods.

Key practices:
- Pin exact versions across all environments (e.g., `version: v1.64.7` instead of `version: v1.64`)
- Use `go install` for Go tools instead of third-party GitHub actions that may become unmaintained
- Explicitly set action parameters even when overriding defaults (e.g., `cache: false` for setup-go)

Example of explicit configuration:
```yaml
- name: Install Go
  uses: actions/setup-go@v4
  with:
    go-version: 1.21.0  # exact version
    cache: false        # explicit cache setting

- name: Install gotestsum
  run: go install gotest.tools/gotestsum@v1.11.0  # exact version via go install
```

This approach ensures reproducible builds, reduces dependency on external maintainers, and makes workflow behavior predictable across different environments and over time.