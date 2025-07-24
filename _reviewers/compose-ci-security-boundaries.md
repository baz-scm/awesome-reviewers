---
title: CI security boundaries
description: Maintain strict security boundaries in CI/CD workflows by treating CI
  as a validation-only system and carefully managing third-party dependencies. CI
  should never automatically modify contributor code or commits - its role is to verify
  that everything is correct, not to replace proper development practices.
repository: docker/compose
label: CI/CD
language: Yaml
comments_count: 3
repository_stars: 35858
---

Maintain strict security boundaries in CI/CD workflows by treating CI as a validation-only system and carefully managing third-party dependencies. CI should never automatically modify contributor code or commits - its role is to verify that everything is correct, not to replace proper development practices.

For third-party GitHub Actions, especially those that are less trusted, pin them to specific commit hashes rather than version tags to prevent supply chain attacks. When upgrading actions, carefully review changes and be aware of new default behaviors that might have security implications.

Example of secure action pinning:
```yaml
# Instead of:
uses: tibdex/github-app-token@v2

# Use:
uses: tibdex/github-app-token@v2.1.0  # or pin to commit hash
```

Be particularly cautious of actions that enable features like provenance generation by default, as these may upload artifacts or require additional permissions. Always explicitly configure such features rather than relying on defaults, and add verification steps to ensure the security chain is complete.