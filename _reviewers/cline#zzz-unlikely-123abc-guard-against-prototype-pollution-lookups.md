---
title: Guard against prototype pollution lookups
description: When indexing a plain object literal with a key derived from untrusted
  or external input (e.g., a file name, extension, or user-provided string), never
  do a bare `obj[key]` lookup. Plain objects inherit from `Object.prototype`, so keys
  like `constructor`, `__proto__`, `toString`, or `hasOwnProperty` will resolve to
  inherited functions/objects instead of...
repository: cline/cline#zzz-unlikely-123abc
label: Security
language: TSX
comments_count: 2
repository_stars: 71035
---

When indexing a plain object literal with a key derived from untrusted or external input (e.g., a file name, extension, or user-provided string), never do a bare `obj[key]` lookup. Plain objects inherit from `Object.prototype`, so keys like `constructor`, `__proto__`, `toString`, or `hasOwnProperty` will resolve to inherited functions/objects instead of `undefined`, leading to unexpected behavior or exploitable logic (a form of prototype pollution). Always verify the key is an own property before returning the lookup, or use a `Map` instead of a plain object/`Record` for untrusted keys.

Example fix pattern:
```ts
function fileIconSpec(path: string): IconSpec {
	const name = baseName(path).toLowerCase();
	const byName = Object.hasOwn(BY_NAME, name) ? BY_NAME[name] : undefined;
	if (byName) return byName;
	...
}
```
Apply the same `Object.hasOwn` guard (or a `Map`) anywhere a `Record<string, T>` is indexed with dynamic, non-literal keys — e.g. extension/language lookup tables, config maps keyed by user input, etc. Add a test case asserting that keys like `"constructor"`, `"__proto__"`, and `"toString"` fall back to the default/neutral value instead of returning an inherited `Object.prototype` member.