---
title: vet third-party actions
description: 'Before using third-party GitHub Actions or similar external dependencies,
  thoroughly review their security implications. Specifically: 1) Understand what
  tokens or credentials they require and how they use them, 2) Verify that permission
  checks and security features work as expected, 3) Avoid providing unnecessary credentials
  (like PATs when not required),...'
repository: prisma/prisma
label: Security
language: Yaml
comments_count: 1
repository_stars: 42967
---

Before using third-party GitHub Actions or similar external dependencies, thoroughly review their security implications. Specifically: 1) Understand what tokens or credentials they require and how they use them, 2) Verify that permission checks and security features work as expected, 3) Avoid providing unnecessary credentials (like PATs when not required), and 4) Add tests to validate the security functionality works correctly.

Example from the discussion:
```yaml
# Before using actions-cool/check-user-permission@v2
# Review: what does it do with tokens? Does it properly check permissions?
- name: Check write permission
  id: check
  uses: actions-cool/check-user-permission@v2
  # Remove PAT if not required, add tests for permission validation
```

This practice prevents security vulnerabilities from poorly understood or misconfigured third-party components and ensures your security controls work as intended.