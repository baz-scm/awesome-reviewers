---
title: Cache Sets In Loops
description: When doing membership checks or repeated filtering, avoid creating derived
  collections (like `new Set(...)`) inside per-item/per-iteration code paths—this
  can silently turn linear work into quadratic work. Even if the code only runs on
  an error/diagnostic path, still cache the derived collection once per outer scope.
repository: facebook/react#b9
label: Performance Optimization
language: TypeScript
comments_count: 2
repository_stars: 251891
---

When doing membership checks or repeated filtering, avoid creating derived collections (like `new Set(...)`) inside per-item/per-iteration code paths—this can silently turn linear work into quadratic work. Even if the code only runs on an error/diagnostic path, still cache the derived collection once per outer scope.

Apply this pattern:
- If you have something like `array.filter(x => new Set(other).has(x))` inside a loop, compute `const set = new Set(other)` once, then reuse it.
- Keep lazy computation for expensive diagnostics only when needed, but don’t build the same expensive structure repeatedly inside that lazy code.

Example (fixing the O(n^2) pattern):
```ts
// Anti-pattern: creates a new Set for each element check
const undefinedIdentifiers = () =>
  (rvaluesUnfiltered.filter(v => new Set(rvalues).has(v)));

// Better: create the Set once
const rvaluesSet = new Set(rvalues);
const undefinedIdentifiers = () => rvaluesUnfiltered.filter(v => rvaluesSet.has(v));
```

If you also add extra full traversals/processing passes, ensure their compile-time cost is either measured and accepted or clearly documented in surrounding comments/docs.