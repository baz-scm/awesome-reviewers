---
title: Null-Safe Access Patterns
description: 'When a value can be nullable (null/undefined), make that fact explicit
  in both types and control flow:


  1) Initialize nullable fields to `null` (don’t leave them uninitialized)'
repository: facebook/react#b2
label: Null Handling
language: JavaScript
comments_count: 10
repository_stars: 251882
---

When a value can be nullable (null/undefined), make that fact explicit in both types and control flow:

1) Initialize nullable fields to `null` (don’t leave them uninitialized)
```js
// Good
let cleanup: null | (() => void) = null;
```

2) Guard before property access, and use optional chaining only when “missing” is a valid state
```js
// Good: ref may be null
const menu = menuRef.current;
if (menu == null) return;

// Good: environment/lifecycle may omit a nested object
devToolsInstance?.bridge.emit('event');
```

3) Use the correct sentinel (`null` vs `undefined`)—don’t paper over type confusion
```js
if (response._debugEndTime === undefined) { /* ... */ }
```

4) Prefer shared helpers for complex null/edge-node behavior (don’t reinvent casts)
- If there’s already a helper that correctly handles “owner/root” resolution, use it instead of bespoke logic.

5) If null indicates a contract violation, fail fast (invariant) rather than silently continuing
- Extra guards are fine only when “missing” is expected by design; otherwise crash so the incorrect assumption gets fixed.
