---
title: Eliminate CI redundancy
description: Design CI/CD pipelines to avoid duplicated or redundant work. Before
  adding a job or step, check whether its output is already produced elsewhere (e.g.,
  don't collect coverage separately for runtimes whose tests already run as part of
  a broader test command) and remove jobs that add no unique value. When the same
  sequence of steps is repeated across...
repository: honojs/Hono
label: CI/CD
language: Yaml
comments_count: 3
repository_stars: 32741
---

Design CI/CD pipelines to avoid duplicated or redundant work. Before adding a job or step, check whether its output is already produced elsewhere (e.g., don't collect coverage separately for runtimes whose tests already run as part of a broader test command) and remove jobs that add no unique value. When the same sequence of steps is repeated across multiple jobs (such as type-check and bundle-check measurement for PR and main variants), extract them into a shared composite action instead of copy-pasting:

```yaml
# .github/actions/perf-measure/action.yml
runs:
  using: "composite"
  steps:
    - run: bun scripts/generate-app.ts
      shell: bash
    - run: bun tsc -p tsconfig.build.json --diagnostics | bun scripts/process-results.ts > diagnostics.json
      shell: bash
```

```yaml
# workflow
steps:
  - uses: ./.github/actions/perf-measure
```

When deciding how to gate a job (e.g., via path filters to skip irrelevant PRs), favor the simpler option of always running it unless the cost is significant, since complex path-based conditions are hard to maintain and risk missing edge cases that affect the measured behavior. This keeps workflows easier to reason about, faster to run, and less error-prone as the pipeline evolves.