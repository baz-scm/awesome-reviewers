---
title: Null-Safe Access Patterns
description: When a value can be null/undefined (or a property may not exist for certain
  node/object kinds), don’t access members directly. Instead, narrow and guard first
  using either (a) explicit null checks/early returns, or (b) type/node-kind checks
  that establish the correct object shape.
repository: facebook/react#b9
label: Null Handling
language: JavaScript
comments_count: 6
repository_stars: 251891
---

When a value can be null/undefined (or a property may not exist for certain node/object kinds), don’t access members directly. Instead, narrow and guard first using either (a) explicit null checks/early returns, or (b) type/node-kind checks that establish the correct object shape.

Practical rules:
- Guard before calling methods/properties: wrap `value.method(...)` / `value.prop` usage with checks that guarantee `value` is non-null and of the expected kind.
- Prefer early-return branches when a ref/handle may be absent; treat “null ref” as an invariant violation when it shouldn’t happen.
- Use the correct null sentinel (`null` vs `undefined`) to match the API/type expectations (don’t introduce a different sentinel just to satisfy the compiler).
- For null checks, match the value space: use `=== null` when the variable is truly null-only; use `== null` or an intentional falsy check only when you mean to cover both null and undefined.

Example:
```js
// Prefer: establish presence before using
const menu = ref.current;
if (menu == null || portalContainer == null || items.length === 0) {
  return; // nothing to do
}
menu.textContent = '...';

// Prefer: narrow by node kind before property access
const ownerDocument =
  otherNode.nodeType === DOCUMENT_NODE
    ? (otherNode: any)
    : otherNode.ownerDocument;

// Prefer: gate method calls
let displayName = showNames ? agent.getComponentNameForHostInstance(node) : null;
if (displayName != null && displayName.startsWith('Forget(')) {
  displayName = '✨' + displayName.slice(7, -1);
}
```