---
title: Cache and Document Costs
description: When code repeatedly allocates helper data structures or re-walks large
  IR/AST fragments inside loops, it can introduce avoidable overhead (including accidental
  O(n²)).
repository: facebook/react#b8
label: Performance Optimization
language: TypeScript
comments_count: 2
repository_stars: 251889
---

When code repeatedly allocates helper data structures or re-walks large IR/AST fragments inside loops, it can introduce avoidable overhead (including accidental O(n²)).

Apply these standards:
1) Cache per-iteration work: if you perform membership checks against a Set/Map repeatedly, create the Set/Map once outside the loop and reuse it.
2) Watch for “walk the whole thing per function” patterns: if you traverse the full source function (or full output) for each compiled unit, add a brief comment with measured/estimated cost and confirm it’s acceptable.
3) Defer expensive computations to rare paths when possible (e.g., only compute diagnostic data on error), but avoid complexity unless it meaningfully reduces work.

Example (cache Set to avoid O(n²)-style behavior):
```ts
// Before: creates a new Set inside the hot path
const undefinedIdentifiers = () =>
  rvaluesUnfiltered.filter(v => new Set(rvalues).has(v));

// After: precompute once and reuse
const rvaluesSet = new Set(rvalues);
const undefinedIdentifiers = () =>
  rvaluesUnfiltered.filter(v => rvaluesSet.has(v));
```

Example (document whole-IR traversal cost):
```ts
// Note: this pass walks the whole source function and the output per compiled function.
// On our fixtures, TS compile time is ~X% higher at the median (profile attributes ~Y%).
// Keeping this despite the cost because it is required for correctness/coverage.
```