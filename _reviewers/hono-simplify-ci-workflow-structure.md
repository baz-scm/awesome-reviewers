---
title: Simplify CI workflow structure
description: 'Design CI/CD workflows to be simple, DRY, and correctly ordered. Specifically:


  1. Avoid duplicating the same sequence of steps across multiple jobs; extract shared
  logic into a composite action (or reusable workflow) so changes only need to be
  made in one place.'
repository: honojs/hono
label: CI/CD
language: Yaml
comments_count: 4
repository_stars: 32741
---

Design CI/CD workflows to be simple, DRY, and correctly ordered. Specifically:

1. Avoid duplicating the same sequence of steps across multiple jobs; extract shared logic into a composite action (or reusable workflow) so changes only need to be made in one place.
2. Only add steps that meaningfully contribute to the workflow's goal — e.g., don't add a "check-only" tool (like a linter that can't autofix) into an `autofix` job; it belongs in a verification job instead.
3. Prefer unconditional, always-run checks over complex path-based or conditional triggers when the check is cheap to run. Fragile file-path filters are hard to maintain and risk silently skipping checks when new files are added; simplicity and safety outweigh the minor cost of running the job every time.
4. Respect step ordering/dependencies: steps that generate code or artifacts required by later steps (e.g., `npm run denoify`) must run before the steps that depend on them (e.g., `npm test`).

Example — extracting duplicated steps into a composite action instead of repeating them in four separate jobs:
```yaml
# .github/actions/perf-measure-type-check/action.yml
runs:
  using: "composite"
  steps:
    - run: bun scripts/generate-app.ts
      shell: bash
    - run: bun tsc -p tsconfig.build.json --diagnostics | bun scripts/process-results.ts > diagnostics.json
      shell: bash
```
Then each job simply calls `uses: ./.github/actions/perf-measure-type-check` instead of repeating the same steps.