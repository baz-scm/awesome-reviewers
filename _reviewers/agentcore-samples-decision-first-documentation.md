---
title: Decision-First Documentation
description: 'When publishing code samples/notebooks, write documentation that is
  (a) decision-first, (b) API-current, and (c) goal-focused.


  1) Add “when to use” differentiation for competing interfaces'
repository: awslabs/agentcore-samples
label: Documentation
language: Other
comments_count: 3
repository_stars: 3244
---

When publishing code samples/notebooks, write documentation that is (a) decision-first, (b) API-current, and (c) goal-focused.

1) Add “when to use” differentiation for competing interfaces
- If the SDK offers multiple runners/tools/strategies, include a comparison section with concrete decision criteria (e.g., orchestration model, result granularity/latency, dataset size, limits/caps, and phases).

Example (template for evaluation runners):
```markdown
| Runner | Orchestration | Results shape | Best for |
|---|---|---|---|
| OnDemandEvaluationDatasetRunner | invoke → wait → evaluate (client-side) | per-scenario detail immediately | CI/dev iteration, small datasets |
| BatchEvaluationRunner | invoke → wait → submit → poll (service-side) | aggregate per-evaluator; detailed sessions in logs | baseline runs, large datasets |
```

2) Remove deprecated/legacy APIs and align naming to modern guidance
- Don’t keep “legacy” client approaches in parallel with recommended APIs.
- Rename notebooks/files so the name encodes the difference (e.g., `*-inbuilt-strategy` vs `*-override-strategy`) and ensure the content uses current, supported APIs.

3) Keep the notebook centered on the teaching objective
- Extract heavy or non-core setup (e.g., agent deployment/build/push/runtime creation) into scripts/utilities.
- In the notebook, start with a short description of the goal, then show only the minimal setup needed to demonstrate the target technique (e.g., evaluation loop/batch polling, memory hook behavior).

Follow-up checklist
- Does each alternative include a “when to use” table/criteria?
- Are there any deprecated interfaces left in the sample?
- Is the notebook’s flow dominated by the concept being taught (not deployment plumbing)?
- Do filenames/notebook titles reflect the actual strategy/interface used?