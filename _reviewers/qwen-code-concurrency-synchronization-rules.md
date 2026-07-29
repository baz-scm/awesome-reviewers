---
title: Concurrency synchronization rules
description: 'Design GitHub Actions concurrency so overlapping runs can’t corrupt
  multi-step outcomes.


  Rules:

  1) Don’t assume `concurrency` is a durable multi-stage queue. If stage A and stage
  B must be serialized as one logical transaction, either:'
repository: QwenLM/qwen-code
label: Concurrency
language: Yaml
comments_count: 4
repository_stars: 26407
---
{% raw %}
Design GitHub Actions concurrency so overlapping runs can’t corrupt multi-step outcomes.

Rules:
1) Don’t assume `concurrency` is a durable multi-stage queue. If stage A and stage B must be serialized as one logical transaction, either:
- Put B in the same concurrency group as A, **or**
- Use per-run isolation for each transaction and make publication idempotent (e.g., unique run IDs + marker-based updates).

2) Align the concurrency group predicate with the job `if` gate. GitHub evaluates concurrency *before* job `if`, so any kill-switch/feature flag that changes run behavior must be included in the concurrency group condition too.

3) Prevent “request accepted, nothing happens”. When concurrency saturation can drop jobs (only one running + one pending), add an always-hosted acknowledgement path (e.g., in `authorize`) that posts a visible “queued/dropped” notice based on in-flight counts.

4) Make publication overwrite-safe:
- Replacing “running” markers must never wipe evidence from a previous terminal report.
- Only update the marker that corresponds to the expected running state (bot-owned + prefix/specific match), otherwise fall back to posting a fresh status.

Example patterns:

A) Same-boundary serialization across dependent stages (use when B must not overlap A):
```yaml
jobs:
  verify:
    concurrency:
      group: ${{ format('{0}-verify-{1}', github.workflow, github.event.issue.number) }}
      cancel-in-progress: false
  publish-verify:
    needs: [verify]
    concurrency:
      group: ${{ format('{0}-verify-{1}', github.workflow, github.event.issue.number) }}
      cancel-in-progress: false
```

B) Per-run isolation + idempotent publication (use when concurrency can’t be made durable):
```yaml
jobs:
  verify:
    concurrency:
      group: ${{ format('{0}-verify-run-{1}', github.workflow, github.run_id) }}
      cancel-in-progress: false
  publish-verify:
    needs: [verify]
    concurrency:
      group: ${{ format('{0}-verify-run-{1}', github.workflow, github.run_id) }}
      cancel-in-progress: false
```

C) Include kill-switch/qualifiers in both `if` and `concurrency.group` (conceptually):
- If `if: vars.MAINTAINER_ECS_RUNNER_DISABLED != 'true'` changes executability,
- then the same condition must be reflected inside the `group:` expression so the same PR doesn’t share groups across modes.

If you apply these principles, your concurrency design becomes correct under race conditions, feature toggles, and saturation—without relying on brittle scheduling assumptions.
{% endraw %}
