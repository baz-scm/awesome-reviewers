---
title: Prevent prototype pollution in lookups
description: When building lookup tables keyed by untrusted or externally-derived
  strings (file names, extensions, paths, user input, etc.), never index a plain object
  literal directly with bracket notation, since values like "constructor", "__proto__",
  "toString", or "hasOwnProperty" will resolve to inherited Object.prototype members
  instead of falling through to your...
repository: cline/cline#&&sleep 4
label: Security
language: TSX
comments_count: 2
repository_stars: 70980
---

When building lookup tables keyed by untrusted or externally-derived strings (file names, extensions, paths, user input, etc.), never index a plain object literal directly with bracket notation, since values like "constructor", "__proto__", "toString", or "hasOwnProperty" will resolve to inherited Object.prototype members instead of falling through to your default/fallback case. This can silently produce wrong behavior and is a classic prototype-pollution-adjacent bug. Always verify the key is an own property before reading it (e.g. `Object.hasOwn(table, key) ? table[key] : fallback`), or use a `Map` instead of a plain object for dynamic lookups, which has no prototype chain to worry about. Add a regression test that exercises dangerous keys such as `constructor`, `__proto__`, and `toString` to confirm they resolve to the default case.

Example:
```ts
// Unsafe: table["constructor"] resolves to Object's constructor function
const icon = BY_EXTENSION[extension] ?? DEFAULT_ICON;

// Safe: only own properties are matched
const icon = Object.hasOwn(BY_EXTENSION, extension)
	? BY_EXTENSION[extension]
	: DEFAULT_ICON;

// Or avoid the issue entirely with a Map
const BY_EXTENSION = new Map<string, IconSpec>([...]);
const icon = BY_EXTENSION.get(extension) ?? DEFAULT_ICON;
```