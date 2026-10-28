---
title: Prevent prototype pollution lookups
description: When using a plain object (`Record<string, T>`) as a lookup table and
  indexing it with a dynamic, externally-derived key (file names, extensions, folder
  names, user input, etc.), never rely on plain bracket access (`table[key]`). Because
  plain objects inherit from `Object.prototype`, keys such as `constructor`, `__proto__`,
  `toString`, or `hasOwnProperty`...
repository: cline/cline#中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中
label: Security
language: TSX
comments_count: 2
repository_stars: 70984
---

When using a plain object (`Record<string, T>`) as a lookup table and indexing it with a dynamic, externally-derived key (file names, extensions, folder names, user input, etc.), never rely on plain bracket access (`table[key]`). Because plain objects inherit from `Object.prototype`, keys such as `constructor`, `__proto__`, `toString`, or `hasOwnProperty` will silently resolve to inherited functions/objects instead of `undefined`, producing incorrect behavior or exploitable prototype-pollution-style bugs. Always verify the key is an own property before returning the value, falling back to a safe default when it is not.

Example:

```ts
function lookup(table: Record<string, IconSpec>, key: string): IconSpec | undefined {
	return Object.hasOwn(table, key) ? table[key] : undefined;
}
```

Apply this pattern consistently to any map/dictionary built from object literals and indexed with untrusted or derived strings, and add a regression test covering keys like `constructor`, `__proto__`, and `toString` to confirm they fall back to the default value instead of returning inherited `Object.prototype` members.