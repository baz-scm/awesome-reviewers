---
title: Validate Algorithmic Assumptions
description: When implementing or changing non-trivial algorithms (selection, merging,
  pagination, estimators, parsing, normalization), explicitly state the invariant/assumption
  and back it with tests that would fail if the assumption is wrong.
repository: cline/cline#v17
label: Algorithms
language: TypeScript
comments_count: 7
repository_stars: 70883
---

When implementing or changing non-trivial algorithms (selection, merging, pagination, estimators, parsing, normalization), explicitly state the invariant/assumption and back it with tests that would fail if the assumption is wrong.

Practical rules:
- Replace naive heuristics with model-based logic (e.g., cost/complexity per item, not proportional to raw payload size). Add tests that compare against a “naive baseline” and prove size-invariance where appropriate.
- Encode dynamic routing/selection invariants directly (e.g., “connected AND still attached”) and skip invalid states rather than relying on timeouts or waiting.
- For parsing/normalization, match the grammar/environment precisely (e.g., YAML precedence + correct line-span for inline vs block scalars; POSIX separator conversion without breaking filenames containing literal backslashes).
- For merge/graph/tree operations with tricky semantics, either document why the operation is safe (e.g., non-overlapping paths) or add a targeted repro test.
- Use property/fuzz tests for state machines/pagination rules (e.g., “skip hides exactly one row; undo restores it”).

Example pattern (invariant/property test):
```ts
// Pseudocode style: assert the invariant that skip hides only one row
fuzzVerbSequences((actions) => {
  const state = runPlugin(actions);
  for (const skip of actions.filter(a => a.verb === "skip")) {
    expect(state.visible).not.toContain(skip.itemId);
  }
  // And the undo property should restore the skipped row
});
```

Checklist before merge:
1) What is the invariant? (e.g., size estimate depends only on item count)
2) What would a naive implementation get wrong?
3) Is there a test that would catch that failure mode (edge-case or randomized)?
4) If the logic depends on subtle runtime semantics, is that semantics either documented or proven by a repro test? 