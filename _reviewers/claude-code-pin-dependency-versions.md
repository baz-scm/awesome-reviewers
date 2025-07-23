---
title: Pin dependency versions
description: Always pin external dependencies to specific commit hashes rather than
  mutable references like tags or branch names to prevent supply chain attacks. This
  applies to GitHub Actions, package dependencies, Docker images, and similar resources
  - even if they're from your own repositories.
repository: anthropics/claude-code
label: Security
language: Yaml
comments_count: 1
repository_stars: 25432
---

Always pin external dependencies to specific commit hashes rather than mutable references like tags or branch names to prevent supply chain attacks. This applies to GitHub Actions, package dependencies, Docker images, and similar resources - even if they're from your own repositories.

If a dependency repository is compromised, using mutable references makes it easier for attackers to execute lateral movement into your project. While using tags like `@latest` or `@beta` is more convenient, it introduces significant security vulnerabilities.

Example:
```yaml
# Insecure - using mutable tag references
- name: Checkout repository
  uses: actions/checkout@v4

# Secure - pinning to specific commit hash
- name: Checkout repository
  uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683  # v4
```

Consider implementing automation to update these hashes regularly while maintaining the security benefits of pinning specific versions.