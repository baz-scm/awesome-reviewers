---
title: Consistent Null Handling
description: 'Use a consistent null/undefined policy and make it explicit in both
  type checks and call/return behavior.


  - **Guard before indexing/access:** when inputs may be missing or null, check the
  right predicate (e.g., `Array.isArray`) and return a consistent “not found” value
  (commonly `undefined`).'
repository: 30-seconds/30-seconds-of-code
label: Null Handling
language: Markdown
comments_count: 6
repository_stars: 129334
---

Use a consistent null/undefined policy and make it explicit in both type checks and call/return behavior.

- **Guard before indexing/access:** when inputs may be missing or null, check the right predicate (e.g., `Array.isArray`) and return a consistent “not found” value (commonly `undefined`).
  ```js
  const head = arr => (Array.isArray(arr) && arr.length ? arr[0] : undefined);
  ```
- **Be explicit about `null` in type logic:** `typeof null === 'object'`, so include a direct `value === null` (and don’t assume `instanceof` covers null).
  ```js
  const isPrimitive = value =>
    !['object', 'function'].includes(typeof value) || value === null;
  ```
- **Avoid `null` sentinels in callback calls when semantics matter:** if a callback’s behavior depends on arguments, prefer **no arguments** (or `undefined`) rather than passing `null`.
  ```js
  const next = () => {
    const fn = fns[curr++];
    fn(fn === last ? undefined : next); // or fn() when you want 0 args
  };
  ```
- **Prefer default parameters over `=== undefined` conditionals:**
  ```js
  const take = (arr, n = 1) => arr.slice(0, n);
  ```

Apply this consistently across helpers to prevent unexpected `undefined` results, null reference errors, and subtle argument-count differences.