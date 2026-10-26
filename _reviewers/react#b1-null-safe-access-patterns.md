---
title: Null-safe Access Patterns
description: 'When a value can be null/undefined (or represents different runtime
  shapes), don’t access properties/methods directly. Instead:


  - Model nullability precisely in types (prefer `null | T` over `void | T` or broad
  unions).'
repository: facebook/react#b1
label: Null Handling
language: JavaScript
comments_count: 8
repository_stars: 251878
---

When a value can be null/undefined (or represents different runtime shapes), don’t access properties/methods directly. Instead:

- Model nullability precisely in types (prefer `null | T` over `void | T` or broad unions).
- Use the correct comparison for the value you expect: if the code can be either null or undefined, prefer `if (x == null) { ... }`; if only one is expected, use `=== null` or `=== undefined` accordingly.
- Narrow by runtime discriminator before property access (e.g., `nodeType`, “document vs shadow root”, etc.) and reuse existing helpers when they already encode correct null behavior.
- For UI/DOM refs, early-return on the same condition that makes the ref unusable (don’t continue with a null ref).

Example (pattern):

```js
function getSafeActiveElement(rootCandidate) {
  // Narrow by runtime shape before accessing .activeElement
  const activeElementRoot =
    rootCandidate.nodeType === DOCUMENT_NODE
      ? rootCandidate
      : getOwnerDocumentFromRootContainer(rootCandidate);

  // Guard null/undefined consistently
  const activeElement = activeElementRoot.activeElement;
  if (activeElement == null) {
    return null;
  }
  return activeElement;
}

function addSignalCleanup(options) {
  // Correct nullable local types
  let signal: null | AbortSignal = null;
  let cleanup: null | (() => void) = null;

  if (options != null && options.signal != null) {
    signal = options.signal;
  }
  // ... later: check cleanup != null before calling
}
```

Applying this consistently prevents type confusion, avoids null reference crashes, and makes Flow/TypeScript (and future readers) align with real runtime behavior.