---
title: Pin Actions SHAs
description: For security-sensitive CI workflows, pin third-party GitHub Actions to
  immutable commit SHAs (not floating tags like `v3`/`v4`). This prevents supply-chain
  risk from upstream tag changes. Use Dependabot (or equivalent) to keep pinned SHAs
  updated automatically.
repository: mermaid-js/mermaid
label: Security
language: Yaml
comments_count: 1
repository_stars: 87952
---

For security-sensitive CI workflows, pin third-party GitHub Actions to immutable commit SHAs (not floating tags like `v3`/`v4`). This prevents supply-chain risk from upstream tag changes. Use Dependabot (or equivalent) to keep pinned SHAs updated automatically.

Example (pinned):
```yml
- uses: actions/checkout@692973e3d937129bcbf40652eb9f2f61becf3332 # v4.1.7
- uses: hadolint/hadolint-action@54c9adbab1582c2ef04b2016b760714a4bfde3cf # v3.1.0
```

Avoid (unpinned/mutable):
```yml
- uses: actions/checkout@4
- uses: hadolint/hadolint-action@3.1.0
```