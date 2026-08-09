---
title: Pin GitHub Actions
description: In CI/CD workflows, mitigate supply-chain risk by ensuring every `uses:`
  action (first- and third-party) is pinned to an immutable full commit SHA, not a
  moving tag/branch. Optionally preserve the intended human version in a trailing
  comment. Also, set critical inputs explicitly when supported (e.g., toolchain selection)
  to keep builds deterministic.
repository: firecrawl/pdf-inspector
label: Security
language: Yaml
comments_count: 1
repository_stars: 13696
---

In CI/CD workflows, mitigate supply-chain risk by ensuring every `uses:` action (first- and third-party) is pinned to an immutable full commit SHA, not a moving tag/branch. Optionally preserve the intended human version in a trailing comment. Also, set critical inputs explicitly when supported (e.g., toolchain selection) to keep builds deterministic.

Example:
```yml
steps:
  - uses: dtolnay/rust-toolchain@<full-commit-sha> # stable
    with:
      toolchain: stable
```
Apply this to all workflow steps that reference actions (`uses:`), including internal or vendored actions.