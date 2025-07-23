---
title: Pin external action dependencies
description: Use full commit hashes instead of version tags when referencing third-party
  GitHub Actions in workflows to prevent unexpected behavior changes if the action
  is modified at its source. This ensures reproducible builds and improves security
  by protecting against supply chain attacks.
repository: openai/codex
label: CI/CD
language: Yaml
comments_count: 2
repository_stars: 31275
---

Use full commit hashes instead of version tags when referencing third-party GitHub Actions in workflows to prevent unexpected behavior changes if the action is modified at its source. This ensures reproducible builds and improves security by protecting against supply chain attacks.

For GitHub's own first-party actions, using semantic versioning tags (like `@v4`) is acceptable since they are widely used and well-maintained, making it easier to identify canonical versions.

Example:
```yaml
steps:
  # Third-party actions: Use full commit hash
  - name: Annotate locations with typos
    uses: codespell-project/codespell-problem-matcher@a8ce06949d771ee07807e8ce2c9b873f906a9fc2 # v1
  - name: Codespell
    uses: codespell-project/actions-codespell@94e0a8e0b7e2a42a1e1223cc80b4c150a38a0e1e # v2
    
  # GitHub first-party actions: Semantic versioning is acceptable
  - name: Checkout
    uses: actions/checkout@v4
```

This practice helps ensure that your CI/CD pipelines remain stable and secure over time, and allows for explicit updating of dependencies when desired rather than automatically adopting potentially breaking changes.