---
title: Safe object-literal lookups
description: When using a plain object literal as a lookup table keyed by external
  or derived strings (file names, extensions, folder names, etc.), avoid direct bracket-access
  lookups like `table[key]`. Because plain objects inherit from `Object.prototype`,
  keys such as `"constructor"`, `"__proto__"`, or `"toString"` resolve to inherited
  members instead of `undefined`,...
repository: cline/cline#中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中
label: Security
language: TSX
comments_count: 2
repository_stars: 70986
---

When using a plain object literal as a lookup table keyed by external or derived strings (file names, extensions, folder names, etc.), avoid direct bracket-access lookups like `table[key]`. Because plain objects inherit from `Object.prototype`, keys such as `"constructor"`, `"__proto__"`, or `"toString"` resolve to inherited members instead of `undefined`, which can leak unexpected values or enable prototype-pollution-style bugs when the key is attacker-influenced (e.g., parsed from a file path, chat message, or diff).

Always verify the key is an own property before using it, or use a structure immune to prototype traversal:

```ts
// Unsafe: `table["constructor"]` returns Object's constructor, not undefined
const spec = BY_EXTENSION[extension];

// Safe: only own properties are considered
const spec = Object.hasOwn(BY_EXTENSION, extension)
	? BY_EXTENSION[extension]
	: undefined;

// Equally safe alternatives:
// - const table = Object.create(null);
// - const table = new Map([...]);
```

Apply this pattern to any lookup table whose keys come from user input, file content, or other untrusted/derived strings, and add a test case covering `constructor`, `__proto__`, and similar prototype-chain property names to confirm they fall back to the default/neutral behavior rather than returning an inherited value.