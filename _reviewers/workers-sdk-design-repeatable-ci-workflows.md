---
title: Design repeatable CI workflows
description: CI workflows should be idempotent and handle cleanup automatically to
  avoid manual intervention and ensure reliable execution. When designing workflows
  that create resources, branches, or temporary artifacts, always include cleanup
  steps that can run safely multiple times.
repository: cloudflare/workers-sdk
label: CI/CD
language: Yaml
comments_count: 2
repository_stars: 3379
---

CI workflows should be idempotent and handle cleanup automatically to avoid manual intervention and ensure reliable execution. When designing workflows that create resources, branches, or temporary artifacts, always include cleanup steps that can run safely multiple times.

Key practices:
- Check for and clean up existing resources before creating new ones
- Use force operations or deletion commands that don't fail if the target doesn't exist
- Design workflows to be safely re-runnable without conflicts

Example from workflow design:
```yaml
- name: "Create Draft PR"
  run: |
    # Clean up existing branch if it exists
    git branch -D run-ci-on-behalf-of-${{ inputs.pr-number }} 2>/dev/null || true
    git checkout -b run-ci-on-behalf-of-${{ inputs.pr-number }}
```

This prevents scenarios where workflows fail on subsequent runs due to existing branches, resources, or conflicts, eliminating the need for manual cleanup and ensuring consistent behavior across executions.