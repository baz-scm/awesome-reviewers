---
title: Guard against prototype pollution
description: When using plain objects as lookup tables/dictionaries keyed by external
  or derived strings (file names, extensions, folder names, user input, etc.), never
  access values with direct bracket notation alone. Doing so lets keys like `constructor`,
  `__proto__`, or `toString` resolve to inherited `Object.prototype` members instead
  of `undefined`, causing...
repository: cline/cline
label: Security
language: TSX
comments_count: 1
repository_stars: 70886
---

When using plain objects as lookup tables/dictionaries keyed by external or derived strings (file names, extensions, folder names, user input, etc.), never access values with direct bracket notation alone. Doing so lets keys like `constructor`, `__proto__`, or `toString` resolve to inherited `Object.prototype` members instead of `undefined`, causing incorrect behavior or exposing a prototype-pollution vector.

Always verify the key is an own property before reading it, e.g. using `Object.hasOwn(table, key)` (or `Object.prototype.hasOwnProperty.call(table, key)`), and fall back to a safe default otherwise:

```ts
function lookup<T>(table: Record<string, T>, key: string, fallback: T): T {
  return Object.hasOwn(table, key) ? table[key] : fallback;
}
```

Alternatively, prefer a `Map` instead of a plain object for dictionaries keyed by untrusted or dynamic strings, since `Map` has no prototype chain to leak. Add regression tests that assert lookups with keys such as `constructor`, `__proto__`, and `toString` return the safe fallback rather than an unexpected inherited value.</description>
</invoke>
