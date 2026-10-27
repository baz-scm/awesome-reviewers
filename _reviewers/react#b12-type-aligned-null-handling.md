---
title: Type-Aligned Null Handling
description: 'When handling potentially missing values, make null safety *type-aligned*
  and *discriminant-driven*.


  Guidelines:

  - **Don’t assume properties exist on all “roots.”** If the value can come from different
  host/document/shadow contexts, select the correct root first, then read the property
  from that root.'
repository: facebook/react#b12
label: Null Handling
language: JavaScript
comments_count: 8
repository_stars: 251896
---

When handling potentially missing values, make null safety *type-aligned* and *discriminant-driven*.

Guidelines:
- **Don’t assume properties exist on all “roots.”** If the value can come from different host/document/shadow contexts, select the correct root first, then read the property from that root.
- **Branch using reliable discriminants** (e.g., `nodeType`, known structural invariants) instead of relying on ad-hoc `as` casts.
- **Match `null` vs `undefined` checks to the declared type.** If a field is `null | T`, check `=== null`; if it’s `T | void`, initialize it explicitly and check consistently.
- **Use Flow narrowing so callsites typecheck.** When a function expects a specific nullability, narrow the variable (often via splitting errored vs normal handler types or early guards) before calling.
- **Initialize nullable fields explicitly to `null`** (avoid uninitialized `void` states) and **guard early** when refs/containers may be null.
- **Fail fast for “should be impossible” states** instead of silently tolerating mismatched shapes.

Example pattern:
```js
// If typed as: const activeElement: ?Element = ...
const root = getHoistableRoot(node);
const activeElement: ?Element = root.activeElement;
if (activeElement == null) {
  return;
}
// safe: activeElement is now non-null
activeElement.blur();

// If typed as: _debugEndTime: null | number
if (response._debugEndTime === null) {
  // ...
}
```

Applying this consistently prevents incorrect property access, inconsistent null comparisons, and unsound casts that bypass Flow/TS guarantees.