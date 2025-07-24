---
title: Streamline workflow configurations
description: Maintain efficient and properly structured CI/CD workflows by removing
  unnecessary dependencies and using consistent formatting patterns. Each workflow
  step should serve a specific purpose for the job it's part of, and matrix configurations
  should follow a consistent structure.
repository: microsoft/typescript
label: CI/CD
language: Yaml
comments_count: 2
repository_stars: 105378
---

Maintain efficient and properly structured CI/CD workflows by removing unnecessary dependencies and using consistent formatting patterns. Each workflow step should serve a specific purpose for the job it's part of, and matrix configurations should follow a consistent structure.

**Remove unnecessary setup steps:**
```yaml
# AVOID: Including unused toolchains or setup steps
- uses: actions/setup-node@49933ea5288caeca8642d1e84afbd3f7d6820020 # v4.4.0
- uses: dtolnay/rust-toolchain@fcf085fcb4b4b8f63f96906cd713eb52181b5ea4 # stable
- uses: ./.github/actions/setup-go

# PREFER: Only include steps required for the specific job
- uses: actions/setup-node@49933ea5288caeca8642d1e84afbd3f7d6820020 # v4.4.0
```

**Use consistent matrix configuration structures:**
```yaml
# PREFER: Use structured objects for better readability and extensibility
runtime:
  - { name: node, version: 20 }
  - { name: node, version: 18 }
  - { name: bun, version: 'latest' }

# For includes, maintain the same structure:
include:
  - { os: ubuntu-latest, runtime: { name: node, version: 20 }, bundle: false }
```

Regular workflow audits should be performed to remove outdated or unnecessary steps that might slow down builds or waste resources. Well-structured workflows are easier to maintain, extend, and debug when issues arise.