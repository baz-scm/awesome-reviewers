---
title: Safe object lookups
description: When indexing a plain object with a dynamically derived key (e.g., a
  file extension, file name, or any externally/user-influenced string), never use
  direct bracket access like `table[key]`. Plain objects inherit from `Object.prototype`,
  so keys such as `"constructor"`, `"__proto__"`, or `"toString"` will silently resolve
  to inherited functions/objects...
repository: cline/cline?ref=main
label: Security
language: TSX
comments_count: 2
repository_stars: 70980
---

When indexing a plain object with a dynamically derived key (e.g., a file extension, file name, or any externally/user-influenced string), never use direct bracket access like `table[key]`. Plain objects inherit from `Object.prototype`, so keys such as `"constructor"`, `"__proto__"`, or `"toString"` will silently resolve to inherited functions/objects instead of `undefined`, causing incorrect behavior or unexpected type confusion.

Always verify the key is an own property before reading it, using `Object.hasOwn(table, key)`, or use a `Map` instead of a plain object literal when the keys come from untrusted/dynamic input. Fall back to a safe default when the key is not an own property.

Example:
```ts
function fileIconSpec(path: string): IconSpec {
	const name = baseName(path).toLowerCase();
	const byName = Object.hasOwn(BY_NAME, name) ? BY_NAME[name] : undefined;
	if (byName) return byName;
	// ... continue with extension/folder lookups using the same guard
	return DEFAULT_ICON;
}
```

Add regression tests exercising poisoning keys such as `"constructor"`, `"__proto__"`, and `"x.constructor"` to confirm they fall back to the default rather than resolving to inherited `Object.prototype` members.