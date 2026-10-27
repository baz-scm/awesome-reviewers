---
title: Null-safe property access
description: 'When a value can be `null`/`undefined`, don’t rely on “guessing” properties
  exist. Instead, narrow explicitly and make the invariant decision clear:


  1) **Narrow before access (or early-return):**'
repository: facebook/react#b4
label: Null Handling
language: JavaScript
comments_count: 7
repository_stars: 251885
---

When a value can be `null`/`undefined`, don’t rely on “guessing” properties exist. Instead, narrow explicitly and make the invariant decision clear:

1) **Narrow before access (or early-return):**
- If the ref/container/root can be absent, branch immediately and return.
- Prefer domain predicates (e.g., node type, root kind) over generic `?.`.

2) **Don’t silently tolerate impossible states:**
- If Flow/types say something can’t happen, don’t paper over it with extra optional checks—use an invariant/throw so you catch parsing/state regressions.

3) **Handle `null` vs `undefined` intentionally:**
- Ensure the code path that distinguishes them is updated (especially memoization/serialization semantics).

Example pattern:
```js
function getSafeOwnerDocument(otherNode) {
  if (otherNode == null) {
    // early return / throw depending on invariants
    return null;
  }
  return otherNode.nodeType === DOCUMENT_NODE
    ? (otherNode: any) // Document.ownerDocument is null
    : otherNode.ownerDocument;
}

function useRefSafely(ref) {
  const el = ref.current;
  if (el == null) {
    // portal not rendered yet; don’t continue
    return;
  }
  el.focus();
}

function traverseExpectedHookTree(next) {
  if (next == null) throw new Error('Expected hook tree');
  // If internal representation promises a structure, don’t add optional guards that hide gaps.
}
```

Apply this consistently in DOM/event code, ref handling, and internal parsing/transitions: explicitly narrow nullable inputs, and fail fast when invariants are violated.