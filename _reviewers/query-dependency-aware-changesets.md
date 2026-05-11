---
title: Dependency-Aware Changesets
description: When using CI/CD release automation based on Changesets, declare only
  the minimal packages that drive the release (so CI/CD doesn’t process redundant
  package updates), and ensure the release workflow is documented in an operationally
  explicit way.
repository: tanstack/query
label: CI/CD
language: Markdown
comments_count: 2
repository_stars: 49380
---

When using CI/CD release automation based on Changesets, declare only the minimal packages that drive the release (so CI/CD doesn’t process redundant package updates), and ensure the release workflow is documented in an operationally explicit way.

**1) Keep changeset package lists minimal (dependency-driven)**
- In the changeset frontmatter, prefer listing the “root” package(s) that cause dependency packages to release automatically.

Example changeset frontmatter:
```md
---
'@tanstack/query-core': patch
---
```

Avoid enumerating many packages unless they truly need independent version bumps.

**2) Document the real CI/CD steps contributors must expect**
- If your pipeline generates a preview PR (Changesets Action) and publishes only after that PR is merged, your contributing/release docs must clearly state:
  - you must create/add a changeset (or ensure one exists)
  - a preview PR will appear and needs review
  - you must merge the preview PR for publishing to NPM

This prevents maintainer surprises and reduces cycle-time confusion when switching release tooling.