---
title: Null Safety and Guards
description: 'Adopt an explicit nullability + guard pattern:


  - Model optional fields with the right type (`null | T` / `?T`) and initialize them
  intentionally (e.g. `let signal: null | AbortSignal = null;`, `cleanup: null | (()
  => void)`), so Flow/TS can force correct handling.'
repository: facebook/react#b15
label: Null Handling
language: JavaScript
comments_count: 7
repository_stars: 251891
---

Adopt an explicit nullability + guard pattern:

- Model optional fields with the right type (`null | T` / `?T`) and initialize them intentionally (e.g. `let signal: null | AbortSignal = null;`, `cleanup: null | (() => void)`), so Flow/TS can force correct handling.
- Never dereference or call methods on values that can be absent. Before access, either:
  1) **Guard with an early return/branch** when a ref/optional value may be null (common for DOM refs and portal refs), or
  2) **Branch on runtime type/kind** when the “right” object (e.g. Document vs ShadowRoot) depends on container/node type.
- Ensure your null/undefined checks match the actual sentinel. Don’t compare `undefined` as if it were `null` (or vice versa).

Example patterns:

```js
// 1) Early return for optional DOM ref
const menu = ref.current;
if (menu == null) {
  return; // portal may be missing
}

// 2) Guard by runtime kind before reading properties
const root = getHoistableRoot(parentInstanceOrContainer);
const activeElement = root.activeElement; // may be null/undefined depending on root
if (activeElement == null) {
  return;
}

// 3) Match the sentinel you actually have
// Prefer checking the actual type used by the codebase:
if (response._debugEndTime === undefined) {
  // ...
}

// 4) Explicit nullable option values
let signal: null | AbortSignal = null;
```

This reduces null reference crashes, avoids “type-confusion” bugs (mixing null vs undefined), and keeps behavior consistent across special cases (documents vs shadow trees, detached containers, missing refs).