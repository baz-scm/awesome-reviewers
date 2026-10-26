---
title: Cache Sets In Loops
description: 'When doing repeated membership/lookup checks in loops (especially in
  compiler/analysis passes), avoid re-creating data structures each iteration.


  **Apply**'
repository: facebook/react#b1
label: Performance Optimization
language: TypeScript
comments_count: 2
repository_stars: 251878
---

When doing repeated membership/lookup checks in loops (especially in compiler/analysis passes), avoid re-creating data structures each iteration.

**Apply**
- If you need `foo in new Set(...)` (or equivalent), build the `Set` (or other index) once outside the loop and reuse it.
- Be wary of accidental **O(n²)** patterns caused by repeated allocation of `Set`/arrays.
- For diagnostic-only paths computed “only on error”, laziness can be fine—but prefer simple code (e.g., an array/set) unless profiling shows the added complexity matters.
- If you add extra full traversals per unit of work, measure and document the cost/regression.

**Example (pattern to fix)**
```ts
// BAD: allocates a new Set each iteration => can become O(n^2)
for (const v of items) {
  if (new Set(otherArray).has(v)) {
    // ...
  }
}
```

**Example (fixed)**
```ts
// GOOD: build once, reuse
const otherSet = new Set(otherArray);
for (const v of items) {
  if (otherSet.has(v)) {
    // ...
  }
}
```

**Rule of thumb**: if a helper constructs a `Set`/map/array based on a collection and is called inside a loop, hoist/cached it unless it’s proven cheap or bounded.