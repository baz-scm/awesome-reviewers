---
title: Null-safe dereferences
description: 'Treat nullability as a runtime concern: before dereferencing or calling
  methods, ensure you’re operating on the correct runtime “shape”, and narrow types
  so Flow and actual values agree.'
repository: facebook/react#b17
label: Null Handling
language: JavaScript
comments_count: 6
repository_stars: 251891
---

Treat nullability as a runtime concern: before dereferencing or calling methods, ensure you’re operating on the correct runtime “shape”, and narrow types so Flow and actual values agree.

Rules:
1) **Guard before access/calls**: if a value can be null/undefined, check it (and any controlling flags) before using properties or methods.
2) **Branch on the real runtime kind**: when null/undefined depends on node/container type, do a `nodeType`/kind check (or use the appropriate helper) rather than assuming properties exist.
3) **Initialize nullable internals with an explicit nullable type** (avoid `void | T` when the real domain is `null | T`).
4) **Prefer fail-fast when invariants are expected**: if types imply non-null but runtime might violate it, crash/throw or otherwise surface the bug instead of silently continuing.
5) **Use `== null` only when you truly mean both null and undefined**; otherwise use precise checks consistent with the nullable domain.

Example pattern:
```js
// 1) Type/shape check before dereference (DOM example)
const ownerDocument =
  node.nodeType === DOCUMENT_NODE
    ? (node: any)
    : node.ownerDocument;

// 2) Guard method calls (ref example)
const el = ref.current;
if (el == null) {
  return; // or throw, depending on whether this is an invariant
}
el.classList.add('x');

// 3) Explicit nullable initialization
let signal: null | AbortSignal = null;
```