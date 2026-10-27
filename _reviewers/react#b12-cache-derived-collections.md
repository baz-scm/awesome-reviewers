---
title: Cache Derived Collections
description: 'In performance-sensitive passes (e.g., compilers/IR transforms), avoid
  recomputing derived collections inside loops.


  **Standard**

  - If you create a `Set`/map/filter result for membership checks or comparisons that
  occurs repeatedly, compute it once and reuse it (or compute it outside the loop).'
repository: facebook/react#b12
label: Performance Optimization
language: TypeScript
comments_count: 2
repository_stars: 251896
---

In performance-sensitive passes (e.g., compilers/IR transforms), avoid recomputing derived collections inside loops.

**Standard**
- If you create a `Set`/map/filter result for membership checks or comparisons that occurs repeatedly, compute it once and reuse it (or compute it outside the loop).
- Watch for accidental **O(n^2)** patterns like “new Set per iteration”.
- When adding additional full-program or full-function traversals, **document the added cost** (complexity and/or measured profiling numbers) so regressions are detectable.

**Example (avoid Set-per-iteration)**
```ts
// ❌ Potential O(n^2): creates a new Set inside a loop
const undefinedIdentifiers = () =>
  someArray.filter(v => new Set(rvalues).has(v));

// ✅ Compute once and reuse
const rvaluesSet = new Set(rvalues);
const undefinedIdentifiers = () =>
  someArray.filter(v => rvaluesSet.has(v));
```

**Application notes**
- Lazy evaluation (e.g., computing error-only diagnostics in a function) is fine *if it demonstrably avoids work*; keep it simple and prefer cached/shared intermediates over recomputation.