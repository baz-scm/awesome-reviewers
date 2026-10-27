---
title: Null-Safe Property Access
description: Before reading a property, ensure the value is both (1) non-null and
  (2) the correct runtime shape. Model nullability precisely in Flow types, initialize
  nullable values to `null` (not `void`), and choose guards that match the real semantics
  (e.g., distinguish `undefined` vs `null` when it affects control flow). If a null/undefined
  path is logically...
repository: facebook/react#b8
label: Null Handling
language: JavaScript
comments_count: 10
repository_stars: 251889
---

Before reading a property, ensure the value is both (1) non-null and (2) the correct runtime shape. Model nullability precisely in Flow types, initialize nullable values to `null` (not `void`), and choose guards that match the real semantics (e.g., distinguish `undefined` vs `null` when it affects control flow). If a null/undefined path is logically impossible based on types/parsing, prefer an invariant/crash over optional chaining.

Example (DOM/root handling):
```js
// Wrong: assumes ownerDocument exists
const activeElement = root.activeElement;

// Correct: guard by node/root kind and use nullable checks
const ownerDocument =
  node.nodeType === DOCUMENT_NODE ? (node: any) : node.ownerDocument;
const active = ownerDocument?.activeElement;
if (active == null) {
  // handle safely
}
```

Checklist:
- Add null guards before dereferencing: `if (x == null) return ...` (use `== null` when you mean null-or-undefined).
- Prefer type/shape checks (`nodeType`, “is DocumentOrShadowRoot”, etc.) over assuming structural properties exist.
- Use `null | T` for nullable fields; initialize `let v: null | T = null;`.
- Don’t use optional chaining (`?.`) to hide impossible states; crash/invariant when types say it can’t happen.
- When `undefined` and `null` differ semantically, don’t treat them as the same in maps/visited-state logic.