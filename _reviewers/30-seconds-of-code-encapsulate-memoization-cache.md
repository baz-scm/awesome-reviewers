---
title: Encapsulate Memoization Cache
description: 'When implementing in-memory caching (e.g., memoization), use a `Map`
  for the cache and keep the cache implementation private.


  - Use `Map` instead of plain objects to avoid prototype/key pitfalls and to support
  non-string keys safely.'
repository: 30-seconds/30-seconds-of-code
label: Caching
language: Markdown
comments_count: 2
repository_stars: 129334
---

When implementing in-memory caching (e.g., memoization), use a `Map` for the cache and keep the cache implementation private.

- Use `Map` instead of plain objects to avoid prototype/key pitfalls and to support non-string keys safely.
- Do not expose the cache object (e.g., via `returnedFn.cache = cache`). External reads/writes can corrupt cached state and cause unpredictable results.

Example (safe memoize):
```js
const memoize = fn => {
  const cache = new Map(); // private
  return value => {
    if (cache.has(value)) return cache.get(value);
    const result = fn(value);
    cache.set(value, result);
    return result;
  };
};
```