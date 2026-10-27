---
title: Cache and Document Hotspots
description: In performance-sensitive compiler/analysis passes, avoid repeated allocations
  or invariant recomputation inside loops (especially creating new lookup Sets repeatedly).
  If the change adds whole-function/whole-output traversals, measure the impact (even
  roughly) and document it so future work can assess regression risk.
repository: facebook/react#b5
label: Performance Optimization
language: TypeScript
comments_count: 2
repository_stars: 251886
---

In performance-sensitive compiler/analysis passes, avoid repeated allocations or invariant recomputation inside loops (especially creating new lookup Sets repeatedly). If the change adds whole-function/whole-output traversals, measure the impact (even roughly) and document it so future work can assess regression risk.

Apply it like this:
- In tight loops, move work that can be computed once (e.g., build a Set for membership tests) out of the loop; reuse it.
- Watch for patterns like `array.filter(x => new Set(arr2).has(x))`—this can silently become O(n^2).
- If you intentionally defer expensive computation to an error-only path, consider whether the added indirection is justified; prefer clarity unless profiling shows it matters.
- When you must walk large IR/AST structures, add a brief cost note (e.g., “~X% median compile-time increase; ~Y% attributed to these walks”) in the PR/description.

Example (cache the Set):
```ts
// Avoid: creates a new Set on every filter iteration
const bad = rvaluesUnfiltered.filter(place =>
  (new Set(rvalues)).has(place),
);

// Prefer: build once, reuse
const rvaluesSet = new Set(rvalues);
const good = rvaluesUnfiltered.filter(place => rvaluesSet.has(place));

// Optional: if expensive work is error-only, compute it only when needed
// (but keep it clear)
let undefinedIdentifiers: null | Place[] = null;
if (compilerErrorDetected) {
  const set = new Set(rvalues);
  undefinedIdentifiers = rvaluesUnfiltered.filter(p => set.has(p));
}
```