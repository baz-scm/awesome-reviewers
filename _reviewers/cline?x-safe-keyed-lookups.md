---
title: Safe keyed lookups
description: When looking up a value in a plain object using a key derived from external
  or user-controlled input (file names, extensions, paths, etc.), never rely on bare
  bracket access (`table[key]`). Plain objects inherit from `Object.prototype`, so
  keys such as `"constructor"`, `"__proto__"`, or `"toString"` will resolve to inherited
  members instead of `undefined`,...
repository: cline/cline?x
label: Security
language: TSX
comments_count: 2
repository_stars: 70983
---

When looking up a value in a plain object using a key derived from external or user-controlled input (file names, extensions, paths, etc.), never rely on bare bracket access (`table[key]`). Plain objects inherit from `Object.prototype`, so keys such as `"constructor"`, `"__proto__"`, or `"toString"` will resolve to inherited members instead of `undefined`, silently returning the wrong value or enabling prototype-pollution-style behavior. Guard every such lookup with an own-property check (`Object.hasOwn(table, key)`) or use a `Map` instead of a plain object, and add a regression test that exercises dangerous keys like `constructor` and `__proto__` to confirm they fall back to the default/safe value.

Example:
```ts
const BY_EXTENSION: Record<string, IconSpec> = { ts: tsIcon, js: jsIcon };

// Unsafe: "constructor".toLowerCase() resolves to Object's constructor function
function unsafeLookup(ext: string) {
	return BY_EXTENSION[ext]; // may return inherited prototype member
}

// Safe: only returns a value if it's an own property
function safeLookup(ext: string) {
	return Object.hasOwn(BY_EXTENSION, ext) ? BY_EXTENSION[ext] : undefined;
}
```