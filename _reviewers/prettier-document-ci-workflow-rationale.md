---
title: Document CI workflow rationale
description: Always include clear comments explaining the reasoning behind CI workflow
  decisions, including test environment separation, version matrix choices, and build
  requirements. This prevents confusion about when different workflows should be used
  and helps maintain consistency across the team.
repository: prettier/prettier
label: CI/CD
language: Yaml
comments_count: 2
repository_stars: 50772
---

Always include clear comments explaining the reasoning behind CI workflow decisions, including test environment separation, version matrix choices, and build requirements. This prevents confusion about when different workflows should be used and helps maintain consistency across the team.

For test workflows, clearly distinguish between development tests (fast, no build required) and production tests (with build artifacts). For version matrices, document the purpose of each version selection:

```yaml
node:
  # Latest even version
  - "20"
  # Minimal version for development  
  - "16"
include:
  - os: "ubuntu-latest"
    # Pick a version that is fast (normally highest LTS version)
    node: "18"
    ENABLE_CODE_COVERAGE: true
```

This documentation helps developers understand which workflow to modify for different types of changes and prevents misplacement of build-dependent steps in development test workflows.