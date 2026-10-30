---
title: Safe dynamic property lookups
description: When indexing a plain object literal with a dynamic, user- or file-derived
  key (e.g. a file extension, name, or path segment), guard against inherited `Object.prototype`
  members such as `constructor`, `__proto__`, or `toString` resolving unexpectedly
  instead of returning your intended default. A lookup like `table[name]` will happily
  return...
repository: cline/cline#"><b>zze3729958
label: Security
language: TSX
comments_count: 2
repository_stars: 71067
---

When indexing a plain object literal with a dynamic, user- or file-derived key (e.g. a file extension, name, or path segment), guard against inherited `Object.prototype` members such as `constructor`, `__proto__`, or `toString` resolving unexpectedly instead of returning your intended default. A lookup like `table[name]` will happily return `Object.prototype.constructor` if `name === "constructor"`, which can leak internals or cause confusing/incorrect behavior and is a known prototype-pollution-adjacent footgun.

Always verify the key is an own property before returning the value, falling back to a safe default otherwise:

```ts
function fileIconSpec(path: string): IconSpec {
	const name = baseName(path).toLowerCase();
	if (Object.hasOwn(BY_NAME, name)) return BY_NAME[name];
	const ext = extensionOf(name);
	if (Object.hasOwn(BY_EXTENSION, ext)) return BY_EXTENSION[ext];
	return DEFAULT_ICON;
}
```

Alternatively, use a `Map` instead of a plain object for lookup tables keyed by external/untrusted strings, since `Map` has no prototype chain to leak through. Add a regression test that exercises keys like `"constructor"`, `"__proto__"`, and `"toString"` to confirm they resolve to the default rather than an inherited value.