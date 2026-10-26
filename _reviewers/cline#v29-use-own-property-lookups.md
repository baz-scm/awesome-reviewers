---
title: Use own-property lookups
description: When using attacker-influenced strings (file paths, extensions, names,
  identifiers, plugin-provided keys) to select values from an object literal, never
  allow prototype/inherited properties to be resolved. Resolve only *own* properties
  (e.g., `Object.hasOwn`) or use `Map`.
repository: cline/cline#v29
label: Security
language: TSX
comments_count: 2
repository_stars: 70893
---

When using attacker-influenced strings (file paths, extensions, names, identifiers, plugin-provided keys) to select values from an object literal, never allow prototype/inherited properties to be resolved. Resolve only *own* properties (e.g., `Object.hasOwn`) or use `Map`.

Apply this anywhere you do `table[someString]` where `someString` may be user/file/plugin controlled.

Example (safe pattern):
```ts
type IconSpec = { icon: unknown; className: string };
const BY_EXTENSION: Record<string, IconSpec> = { ts: { icon: /*...*/, className: "..." } };

function iconSpecForExtension(ext: string): IconSpec {
  const key = ext.toLowerCase();
  if (Object.hasOwn(BY_EXTENSION, key)) return BY_EXTENSION[key];
  return { icon: /* neutral */, className: "text-muted-foreground" };
}
```

Also add regression tests that verify lookups for keys like `"__proto__"`, `"constructor"`, and `"toString"` do not return any real entries (and fall back to the neutral/default behavior).