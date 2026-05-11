---
title: Null-Safe Optional Handling
description: When dealing with possibly missing or nullable values (especially globals
  and config), make null/undefined handling explicit and never call a value unless
  you’ve verified its type.
repository: tanstack/query
label: Null Handling
language: JavaScript
comments_count: 2
repository_stars: 49380
---

When dealing with possibly missing or nullable values (especially globals and config), make null/undefined handling explicit and never call a value unless you’ve verified its type.

Apply this standard:
- Use explicit checks for undefined: `x === undefined` (or `x !== undefined`) rather than relying on implicit truthiness.
- Guard optional callbacks: before calling `maybeFn(...)`, ensure `typeof maybeFn === 'function'`.
- If refactoring boolean logic around undefined/missing values, add/adjust unit tests to confirm behavior is unchanged.

Example:
```js
function isDocumentVisible(document) {
  return (
    document.visibilityState === undefined ||
    document.visibilityState === 'visible' ||
    document.visibilityState === 'prerender'
  );
}

function shouldRetry(query, error) {
  const retry = query.config.retry;

  if (retry === true) return true;
  if (typeof retry === 'number') return query.state.failureCount <= retry;
  if (typeof retry === 'function') {
    return retry(query.state.failureCount, error);
  }
  return false;
}
```