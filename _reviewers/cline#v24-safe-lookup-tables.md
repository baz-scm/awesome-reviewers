---
title: Safe lookup tables
description: When you use plain objects as lookup tables (e.g., mapping filenames/extensions
  to behavior), treat the lookup key as untrusted. Prevent prototype/inherited-property
  resolution (e.g., `__proto__`, `constructor`, `toString`) by using an own-property
  check (e.g., `Object.hasOwn`) or by switching to `Map`, and always fall back to
  a safe default.
repository: cline/cline#v24
label: Security
language: TSX
comments_count: 2
repository_stars: 70891
---

When you use plain objects as lookup tables (e.g., mapping filenames/extensions to behavior), treat the lookup key as untrusted. Prevent prototype/inherited-property resolution (e.g., `__proto__`, `constructor`, `toString`) by using an own-property check (e.g., `Object.hasOwn`) or by switching to `Map`, and always fall back to a safe default.

Example (own-property guard):
```ts
type IconSpec = { /* ... */ };
const BY_EXTENSION: Record<string, IconSpec> = { /* ... */ };

export function lookupByExtension(key: string): IconSpec {
  const normalized = key.toLowerCase();
  return Object.hasOwn(BY_EXTENSION, normalized)
    ? BY_EXTENSION[normalized]
    : /* safe default */ BY_EXTENSION["default"];
}
```

Apply this anywhere a lookup table is indexed by values derived from file paths, URLs, user input, or other external sources—especially when the table is a `Record`/object literal.