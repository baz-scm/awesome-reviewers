---
title: Intentional Null Guards
description: When dealing with nullable values, never access members/methods (e.g.
  `activeElement`, `startsWith`, `ownerDocument`, `bridge.emit`) unless you’ve narrowed
  the value to the correct non-null type. Also choose null comparisons/operators intentionally.
repository: facebook/react#b11
label: Null Handling
language: JavaScript
comments_count: 10
repository_stars: 251894
---

When dealing with nullable values, never access members/methods (e.g. `activeElement`, `startsWith`, `ownerDocument`, `bridge.emit`) unless you’ve narrowed the value to the correct non-null type. Also choose null comparisons/operators intentionally.

Rules:
- Guard before dereferencing: derive the nullable receiver from the correct domain, then check for null/undefined before reading properties.
- Match `== null` vs `=== null` to your intent:
  - Use `x == null` only when you mean “null or undefined”.
  - Use `x === null` (or `typeof x === 'undefined'`) when you mean exactly one case.
- For “impossible” states: prefer an explicit crash/invariant so we surface parsing/typing gaps early; don’t silently continue.
- Keep local nullable variables aligned with their type so type-narrowing works as expected.

Example pattern:
```js
function safeStartsWith(value: ?string, prefix: string): boolean {
  if (value == null) return false; // null or undefined
  return value.startsWith(prefix);
}

// Intentional exact-null check
function renderMaybe(div: null | HTMLElement) {
  if (div === null) return;
  // div is HTMLElement here
}
```

Apply this especially in DOM/ShadowRoot/document-position code paths and in any logic that may receive missing/optional entries (refs, parsed metadata, backend-produced values).