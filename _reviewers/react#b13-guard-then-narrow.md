---
title: Guard then Narrow
description: 'When a value can be `null`/`undefined` (or a union can include “not-ready”
  shapes), do two things before using it:


  1) **Guard explicitly** before any property/method access. Use clear early returns/branches
  so nullable values never reach the unsafe code path.'
repository: facebook/react#b13
label: Null Handling
language: JavaScript
comments_count: 7
repository_stars: 251893
---

When a value can be `null`/`undefined` (or a union can include “not-ready” shapes), do two things before using it:

1) **Guard explicitly** before any property/method access. Use clear early returns/branches so nullable values never reach the unsafe code path.
2) **Narrow at the call site** (via guard branching or small type splits) so the type checker can prove the passed value matches the callee’s expectations—avoid “papering over” with casts/fixes.
3) **Respect invariants**: if internal logic says a state must exist, prefer an `invariant`/`throw` over optional chaining or silent fallbacks.
4) **Use correct null semantics**: prefer `value == null` when you mean “`null` or `undefined`”; prefer `value === null` only when `undefined` is not expected. Also initialize nullable vars to the sentinel your code expects (often `null`, not `void`).

Example pattern:
```js
function doWork(node: ?{activeElement?: any}, showNames: boolean) {
  // 1) guard
  if (node == null) return;

  // 3) invariant: only parse when enabled
  if (!showNames) return;

  // 2) narrow before access
  const activeElement = node.activeElement;
  if (activeElement == null) return;

  // safe to use
  return activeElement.getBoundingClientRect();
}
```

Applying this consistently prevents both runtime `TypeError`s (unguarded property access) and type/semantic bugs (passing the wrong union member into downstream helpers).