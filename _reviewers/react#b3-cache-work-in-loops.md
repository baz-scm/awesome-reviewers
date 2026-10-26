---
title: Cache Work In Loops
description: In performance-sensitive compiler/IR code, avoid repeated allocations
  and whole-structure recomputation inside loops/filters. If you intentionally perform
  expensive full walks (e.g., multiple traversals per compiled function), document
  the cost and verify via profiling/benchmarks.
repository: facebook/react#b3
label: Performance Optimization
language: TypeScript
comments_count: 2
repository_stars: 251883
---

In performance-sensitive compiler/IR code, avoid repeated allocations and whole-structure recomputation inside loops/filters. If you intentionally perform expensive full walks (e.g., multiple traversals per compiled function), document the cost and verify via profiling/benchmarks.

**What to do**
- Move any `new Set(...)` / derived collection construction out of repeated callbacks/loops.
- Prefer computing once, then reusing in `filter/map` predicates.
- If the algorithm requires multiple full traversals, add a short note (and ideally measured impact) near the algorithm description so future changes don’t unknowingly compound cost.

**Example (avoid O(n^2))**
```ts
// Before: builds a new Set for each iteration -> O(n^2)
const rvalues = rvaluesUnfiltered.filter(place =>
  !inScope(...) || rvaluesUnfiltered.filter(v => /* ... */).includes(place)
);

// After: cache once
const allowed = new Set(rvaluesUnfiltered);
const rvalues = rvaluesUnfiltered.filter(place =>
  !inScope(...) || allowed.has(place)
);
```

**Also apply**
- For intentional multi-pass logic: add a brief “cost” comment (e.g., “walks source + output once per compiled function; median compile +X%; profile shows ~Y% here”) to keep performance expectations clear.