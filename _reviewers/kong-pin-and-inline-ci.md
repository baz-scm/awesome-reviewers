---
title: Pin and Inline CI
description: Harden CI/CD workflows by (1) pinning external actions/tool versions,
  (2) minimizing opaque third-party action wrappers when the underlying steps are
  small and deterministic, and (3) scoping dependency installation to the right workflow
  (local dev vs CI).
repository: Kong/kong
label: CI/CD
language: Yaml
comments_count: 3
repository_stars: 43871
---

Harden CI/CD workflows by (1) pinning external actions/tool versions, (2) minimizing opaque third-party action wrappers when the underlying steps are small and deterministic, and (3) scoping dependency installation to the right workflow (local dev vs CI).

Apply these rules:
- Pin official actions/tooling to a specific version (avoid floating tags). If the organization has a policy for commit SHAs, follow it; otherwise use the action’s explicit version label for consistency.
- For simple tasks implemented by a third-party action that mainly runs a short command sequence, prefer maintaining the equivalent commands directly in your workflow (or a small in-repo script) to reduce audit/lock-down surface.
- Only add dependencies to common developer targets (e.g., `make dev`) when they are broadly needed. If a dependency is specialized/soon-to-change, keep it in CI where it’s required.

Example pattern:
```yaml
- name: Lock Go version
  uses: actions/setup-go@v5
  with:
    go-version: '1.21'

- name: Install CI-only test dependency
  run: |
    make dev
    pip install kong-pdk
```