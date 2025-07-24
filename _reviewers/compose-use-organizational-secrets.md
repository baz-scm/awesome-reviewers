---
title: Use organizational secrets
description: When working with GitHub Actions workflows that require shared credentials
  or tokens, leverage organizational-level secrets instead of duplicating them across
  individual repositories. This approach centralizes secret management, reduces the
  attack surface, and simplifies maintenance.
repository: docker/compose
label: Security
language: Yaml
comments_count: 1
repository_stars: 35858
---

When working with GitHub Actions workflows that require shared credentials or tokens, leverage organizational-level secrets instead of duplicating them across individual repositories. This approach centralizes secret management, reduces the attack surface, and simplifies maintenance.

Organizational secrets should be used for credentials that are shared across multiple repositories within the same organization, such as deployment tokens, API keys for shared services, or documentation dispatch tokens.

Example from a GitHub Actions workflow:
```yaml
steps:
  - name: Sending event to upstream repository
    uses: actions/github-script@v6
    with:
      github-token: ${{ secrets.GHPAT_DOCS_DISPATCH }}
```

In this case, `GHPAT_DOCS_DISPATCH` should be configured at the organization level rather than being added to each individual repository that needs it. This ensures consistent access control, easier rotation of credentials, and prevents secret sprawl across repositories.