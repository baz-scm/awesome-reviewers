---
title: Explicit Null Guards
description: When code can encounter `null`/`undefined`, make nullability explicit
  in both types and control flow—then dereference only after guarding, and use the
  correct API/helper to derive the object you intend to read.
repository: facebook/react#b7
label: Null Handling
language: JavaScript
comments_count: 7
repository_stars: 251888
---

When code can encounter `null`/`undefined`, make nullability explicit in both types and control flow—then dereference only after guarding, and use the correct API/helper to derive the object you intend to read.

Practical rules:
- **Guard before access**: If a value can be missing (e.g., a ref, container-derived root, or optional platform property), branch/early-return before reading its fields.
- **Match runtime reality with types**: If the runtime uses `null`, prefer `null | T` (and initialize to `null`). Avoid `void | T` when you mean “nullable value”.
- **Be consistent about `null` vs `undefined`**: Ensure your checks and Flow types agree (`undefined` vs `null` mismatches are a common source of unsound code).
- **Derive ownership/root correctly**: Don’t assume the object you currently have exposes DOM/shadow properties—use an existing helper (or branch on node/container type) to pick the correct `DocumentOrShadowRoot`/owner before reading fields.

Example pattern:
```js
function safeReadActiveElement(container: any) {
  // Derive the correct root/document first.
  const root = getHoistableRoot(container); // or getOwnerDocumentFromRootContainer(...)

  // Make nullability explicit.
  const active: ?Element = root.activeElement;
  if (active == null) {
    return null;
  }
  return active;
}

function addListener(dom: any, options?: any) {
  // Prefer nullability that matches runtime/type.
  let signal: null | AbortSignal = null;
  if (options != null && options.signal != null) {
    signal = options.signal;
  }
  // Guard any optional object before deref.
  // ...
}
```
This prevents property-access crashes, avoids silent behavior differences across `null`/`undefined`, and keeps Flow/type narrowing aligned with actual runtime behavior.