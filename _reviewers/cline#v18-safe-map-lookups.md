---
title: Safe Map Lookups
description: When you derive behavior from untrusted path/filename/extension strings
  (e.g., selecting an icon or syntax highlighter), never rely on plain object indexing
  alone. Ensure you only accept *own* properties and treat inherited/prototype keys
  (like `__proto__`, `constructor`, `toString`) as invalid.
repository: cline/cline#v18
label: Security
language: TSX
comments_count: 2
repository_stars: 70884
---

When you derive behavior from untrusted path/filename/extension strings (e.g., selecting an icon or syntax highlighter), never rely on plain object indexing alone. Ensure you only accept *own* properties and treat inherited/prototype keys (like `__proto__`, `constructor`, `toString`) as invalid.

Apply this rule:
- Store mappings in objects and check keys with `Object.hasOwn(mapping, key)` (or use `Object.create(null)` plus `hasOwn`).
- If the key is not an own property, fall back to a neutral/default behavior.

Example:
```ts
type Spec = { /* ... */ };
const BY_EXTENSION: Record<string, Spec> = {
  ts: { /* ... */ },
  // ...
};

export function specForPath(path: string): Spec | undefined {
  const name = path.split(/[\\/]/).pop() ?? path;
  const ext = name.includes('.') ? (name.split('.').pop() ?? '').toLowerCase() : '';

  return Object.hasOwn(BY_EXTENSION, ext) ? BY_EXTENSION[ext] : undefined;
}
```

This prevents surprising resolution of inherited members when inputs contain prototype-related keys, reducing security risk and improving correctness.