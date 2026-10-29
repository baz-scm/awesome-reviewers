---
title: Guard against prototype pollution
description: When looking up values in a plain object using a dynamic, externally-derived
  string as the key (e.g., a filename, extension, or folder name), never use direct
  bracket access like `table[key]`. Because plain objects inherit from `Object.prototype`,
  keys such as `constructor`, `__proto__`, or `toString` will resolve to inherited
  properties instead of...
repository: cline/cline#1
label: Security
language: TSX
comments_count: 1
repository_stars: 71024
---

When looking up values in a plain object using a dynamic, externally-derived string as the key (e.g., a filename, extension, or folder name), never use direct bracket access like `table[key]`. Because plain objects inherit from `Object.prototype`, keys such as `constructor`, `__proto__`, or `toString` will resolve to inherited properties instead of `undefined`, leading to unexpected behavior or security issues (prototype pollution / unintended code execution paths).

Always verify the key is an own property before accessing it, using `Object.hasOwn(table, key)` (or `Object.prototype.hasOwnProperty.call(table, key)`), or prefer a `Map` for key-value lookups driven by untrusted input, since `Map` has no prototype chain to collide with.

Example fix:
```ts
function lookup(table: Record<string, IconSpec>, key: string): IconSpec | undefined {
	return Object.hasOwn(table, key) ? table[key] : undefined;
}
```

Add a regression test covering dangerous keys like `"constructor"`, `"__proto__"`, and `"toString"` to confirm they fall back to the default/neutral behavior instead of returning inherited object properties.