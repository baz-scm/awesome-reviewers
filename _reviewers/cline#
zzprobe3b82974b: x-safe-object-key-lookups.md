---
title: Safe object key lookups
description: When using plain JavaScript/TypeScript objects as lookup tables (e.g.,
  `Record<string, T>`) keyed by external or user-derived strings (file names, extensions,
  folder names, etc.), never access properties with direct bracket/dot notation alone.
  Untrusted keys such as `constructor`, `__proto__`, or `toString` will resolve to
  inherited `Object.prototype`...
repository: 'cline/cline#

  zzprobe3b82974b: x'
label: Security
language: TSX
comments_count: 1
repository_stars: 71067
---

When using plain JavaScript/TypeScript objects as lookup tables (e.g., `Record<string, T>`) keyed by external or user-derived strings (file names, extensions, folder names, etc.), never access properties with direct bracket/dot notation alone. Untrusted keys such as `constructor`, `__proto__`, or `toString` will resolve to inherited `Object.prototype` members instead of `undefined`, causing incorrect behavior or potential prototype-pollution-style exploits. Always verify the key is an own property before using the lookup value, e.g. via `Object.hasOwn(table, key)` (or `Object.prototype.hasOwnProperty.call(table, key)`), falling back to a safe default when the check fails. Prefer `Map` instances over plain objects for dictionaries built from untrusted input, since `Map` has no prototype chain to leak.

Example:
```ts
function lookup(table: Record<string, IconSpec>, key: string): IconSpec | undefined {
  return Object.hasOwn(table, key) ? table[key] : undefined;
}
```
Add regression tests covering dangerous keys like `"constructor"`, `"__proto__"`, and `"toString"` to confirm they fall back to the default/neutral value instead of leaking prototype methods.