---
title: Use canonical invariants
description: When implementing algorithmic parsing/validation, base ordering/state
  on the canonical structured source, and keep validation logic split by invariant
  (local vs global) with explicit intent.
repository: freeCodeCamp/freeCodeCamp
label: Algorithms
language: JavaScript
comments_count: 2
repository_stars: 444449
---

When implementing algorithmic parsing/validation, base ordering/state on the canonical structured source, and keep validation logic split by invariant (local vs global) with explicit intent.

How to apply:
- Prefer authoritative structured data over heuristic text scanning. If the algorithm needs “step order” or similar ordering/state, derive it from the relevant JSON (or other canonical artifact) rather than from frontmatter or partial text.
- If you have multiple checks that seem redundant, treat them as enforcing different invariants:
  - Local invariant (e.g., per-file constraint like “no single seed file has >2 markers”).
  - Global invariant (e.g., workshop constraint like “exactly 2 total markers across all seed files”).
- Document the invariant split inline so future refactors don’t remove a “redundant” check that actually guards a different failure mode.

Example pattern (sketch):
```js
const fs = require('fs');

function getStepOrder(blockJsonPath) {
  const block = JSON.parse(fs.readFileSync(blockJsonPath, 'utf8'));
  return block.steps.map(s => s.order); // derive ordering from canonical data
}

function isLastStep(stepOrder, currentOrder) {
  return currentOrder === Math.max(...stepOrder);
}

function validateSeeds(seeds) {
  // Local invariant: per-seed-file
  for (const seed of seeds) {
    const markers = findRegionMarkers(seed);
    if (markers > 2) throw new Error('Per-file: too many markers');
  }

  // Global invariant: across all seeds
  const totalMarkers = seeds.reduce((sum, seed) => sum + countMarkers(seed), 0);
  if (totalMarkers !== 2) throw new Error('Workshop: exactly two total markers');
}
```

This approach improves algorithmic reliability (correct ordering/state) and correctness of constraint enforcement (no accidental gaps from removing “seemingly redundant” checks).