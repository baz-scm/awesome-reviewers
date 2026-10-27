---
title: Null-Safe Dereferencing
description: 'Always reconcile *runtime nullability* with *static types* before dereferencing:


  - **Narrow first, then access**: if a value can be null/undefined or a different
  runtime shape, branch (often by node/type/container type) before reading properties.'
repository: facebook/react#b16
label: Null Handling
language: JavaScript
comments_count: 10
repository_stars: 251891
---

Always reconcile *runtime nullability* with *static types* before dereferencing:

- **Narrow first, then access**: if a value can be null/undefined or a different runtime shape, branch (often by node/type/container type) before reading properties.
- **Use the correct sentinel everywhere**: if a type is `null | T`, initialize with `null` and compare against `null` (not `undefined`). Keep null/undefined semantics consistent across the codebase.
- **Prefer shared helpers for complex shapes**: when multiple callsites need owner/root resolution, reuse the same helper rather than ad-hoc casts.
- **Fail fast for impossible states**: if logic/types say a value should exist, don’t “optional-chain away” the invariant—narrow so it’s provably safe or throw.
- **Don’t break boolean logic with null-safety syntax**: optional chaining/non-null checks must preserve the intended condition.

Example (pattern):
```js
// If activeElementRoot can be null/undefined, narrow before deref.
const activeElementRoot = getHoistableRoot(parentInstanceOrContainer);
const activeElement = activeElementRoot.activeElement; // only after correct root choice
if (activeElement == null) {
  // ...
}

// If a field is declared `null | number`, check for null.
if (response._debugEndTime === null) {
  // ...
}

// If an invariant should never fail, don’t mask it.
if (prevHooks == null || nextHooks == null) {
  return null; // or throw, depending on the invariant
}
```

Adopting this prevents missing-property crashes, incorrect comparisons (`null` vs `undefined`), and “silent correctness” bugs caused by optional-chaining over real logic gaps.