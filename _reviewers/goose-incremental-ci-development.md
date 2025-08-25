---
title: Incremental CI development
description: Develop CI/CD workflows incrementally, starting with simpler versions
  and adding complexity gradually. This approach makes testing easier and reduces
  the risk of introducing breaking changes. When adding new steps or jobs, consider
  their performance impact and dependencies on other workflow components.
repository: block/goose
label: CI/CD
language: Yaml
comments_count: 2
repository_stars: 19037
---

Develop CI/CD workflows incrementally, starting with simpler versions and adding complexity gradually. This approach makes testing easier and reduces the risk of introducing breaking changes. When adding new steps or jobs, consider their performance impact and dependencies on other workflow components.

Start by implementing basic functionality first, then progressively add advanced features like release automation or complex build matrices. For example, when creating a new build workflow, begin with a single architecture or platform, test thoroughly, then expand to multiple targets.

When adding new CI steps, evaluate whether they should run in parallel jobs or be integrated into existing ones based on dependencies and performance considerations. Monitor build times and be prepared to refactor job organization if performance degrades.

Example approach:
```yaml
# Phase 1: Basic build only
- name: build
  run: cargo build --release

# Phase 2: Add testing after basic build is stable  
- name: test
  run: cargo test

# Phase 3: Add release automation once build/test is proven
- name: release
  if: github.ref == 'refs/heads/main'
  run: ./scripts/release.sh
```

This incremental strategy helps identify issues early and makes workflow changes easier to debug and maintain.