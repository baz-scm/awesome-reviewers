---
title: Single-writer parallel join
description: 'When using concurrency/parallel subagents, enforce synchronization and
  determinism:


  1) Parallelize independent work

  - Start independent steps concurrently (e.g., multiple subagents), each operating
  on immutable inputs.'
repository: bmad-code-org/bmad-method
label: Concurrency
language: Markdown
comments_count: 2
repository_stars: 51859
---

When using concurrency/parallel subagents, enforce synchronization and determinism:

1) Parallelize independent work
- Start independent steps concurrently (e.g., multiple subagents), each operating on immutable inputs.

2) Join before dependent stages
- Wait for all parallel steps to complete before moving to any stage that depends on their outputs.

3) Single-writer rule for shared state
- Make workers/subagents return structured results (digests/messages) only.
- Ensure exactly one “lead/orchestrator” performs side effects that mutate shared state (e.g., writing `research.md`).

4) Preserve deterministic ordering
- If outputs must be committed “in plan order” or another specific sequence, have the lead commit in that order after the join.

Example (orchestrated parallel workers with single writer):
```ts
async function runPlan(planDims: Dimension[], runWorkers: (d: Dimension) => Promise<Digest>) {
  // 1) parallel: gather all digests for a phase
  const digests = await Promise.all(planDims.map(runWorkers));

  // 2) single-writer: commit sequentially in required order
  for (const d of planDims) {
    const digest = digests[planDims.indexOf(d)];
    researchMd.append(renderDimensionSection(d, digest));
  }
}
```
Apply this especially when multiple concurrent agents could otherwise race on files, database rows, or shared in-memory structures.