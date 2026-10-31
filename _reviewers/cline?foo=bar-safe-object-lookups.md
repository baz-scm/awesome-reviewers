---
title: Safe object lookups
description: When indexing a plain JavaScript object with a key derived from external
  or user-controlled input (e.g., a file extension, path segment, or header value),
  guard against prototype pollution and unintended inherited-property access. A lookup
  like `EXTENSION_LANGUAGES[extension]` will silently resolve to inherited `Object.prototype`
  members (e.g.,...
repository: cline/cline?foo=bar
label: Security
language: TSX
comments_count: 1
repository_stars: 71082
---

When indexing a plain JavaScript object with a key derived from external or user-controlled input (e.g., a file extension, path segment, or header value), guard against prototype pollution and unintended inherited-property access. A lookup like `EXTENSION_LANGUAGES[extension]` will silently resolve to inherited `Object.prototype` members (e.g., `constructor`, `__proto__`, `toString`) if the attacker-controlled key happens to match one, leading to unexpected or exploitable behavior.

Always verify the key is an own property before using the value, or use a structure immune to prototype chain lookups:

```ts
// Unsafe: "constructor" or "__proto__" resolve to inherited members
return EXTENSION_LANGUAGES[extension] ?? extension;

// Safe: only match own, explicitly defined keys
return Object.hasOwn(EXTENSION_LANGUAGES, extension)
  ? EXTENSION_LANGUAGES[extension]
  : extension;

// Alternative: use a Map or Object.create(null) for the table itself
const EXTENSION_LANGUAGES = new Map([["cts", "typescript"], ...]);
```

Apply this pattern to any lookup table, cache, or config object keyed by untrusted input, and add a regression test that exercises keys like `constructor`, `__proto__`, and `toString`.