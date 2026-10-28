---
title: Guard dynamic object lookups
description: When indexing a plain object with a key derived from external or user-controlled
  input (file names, extensions, paths, etc.), never rely on direct bracket access
  (`obj[key]`) or the `in` operator, since plain objects inherit from `Object.prototype`.
  Keys such as `"constructor"`, `"__proto__"`, or `"toString"` will resolve to inherited
  members instead of...
repository: cline/cline#|sleep 4
label: Security
language: TSX
comments_count: 2
repository_stars: 70979
---

When indexing a plain object with a key derived from external or user-controlled input (file names, extensions, paths, etc.), never rely on direct bracket access (`obj[key]`) or the `in` operator, since plain objects inherit from `Object.prototype`. Keys such as `"constructor"`, `"__proto__"`, or `"toString"` will resolve to inherited members instead of `undefined`, leading to incorrect behavior or prototype-pollution-style vulnerabilities.

Always verify the key is an own property before reading it, using `Object.hasOwn(obj, key)` (or `Object.prototype.hasOwnProperty.call`), or prefer a `Map` when the keyset is fully dynamic:

```ts
function lookup<T>(table: Record<string, T>, key: string): T | undefined {
  return Object.hasOwn(table, key) ? table[key] : undefined;
}

// instead of:
const spec = BY_EXTENSION[extension]; // vulnerable: extension could be "constructor"
```

Add regression tests exercising dangerous keys (`constructor`, `__proto__`, `toString`, `x.constructor`) to confirm they fall back to the default/neutral behavior rather than leaking prototype members.</description>
