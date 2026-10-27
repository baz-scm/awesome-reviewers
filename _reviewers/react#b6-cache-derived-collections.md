---
title: Cache Derived Collections
description: When building compiler analyses/transforms, prevent accidental quadratic
  behavior and repeated work by caching derived collections and documenting unavoidable
  full traversals.
repository: facebook/react#b6
label: Performance Optimization
language: TypeScript
comments_count: 2
repository_stars: 251888
---

When building compiler analyses/transforms, prevent accidental quadratic behavior and repeated work by caching derived collections and documenting unavoidable full traversals.

Apply this rule:
- If a pass does full scans “once per function” (or similar), measure/spot-check and leave a brief note describing the expected overhead.
- Inside loops (including error-report paths), do not repeatedly construct derived structures like `new Set(...)` that are reused across iterations. Hoist the construction out of the loop.

Example (avoid repeated `Set` creation):
```ts
// BAD: creates a new Set per iteration -> potential O(n^2)
const undefinedIdentifiers = () =>
  placesToCheck
    .filter(v => new Set(memoized).has(v));

// GOOD: create the Set once, reuse it in the loop
const memoizedSet = new Set(memoized);
const undefinedIdentifiers = () =>
  placesToCheck.filter(v => memoizedSet.has(v));
```

Also, if you intentionally traverse large structures, add a short comment with the measured/estimated cost so performance regressions are easier to detect later.