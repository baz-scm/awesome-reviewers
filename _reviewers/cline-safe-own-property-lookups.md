---
title: Safe Own-Property Lookups
description: When you look up values in plain objects using strings derived from user
  input (e.g., file paths, names, extensions), only accept *own* properties. Use `Object.hasOwn(...)`
  (or `Object.prototype.hasOwnProperty.call`) so special/inherited keys like `__proto__`,
  `constructor`, and `toString` can’t influence results.
repository: ClInE/cLiNe
label: Security
language: TSX
comments_count: 2
repository_stars: 70838
---

When you look up values in plain objects using strings derived from user input (e.g., file paths, names, extensions), only accept *own* properties. Use `Object.hasOwn(...)` (or `Object.prototype.hasOwnProperty.call`) so special/inherited keys like `__proto__`, `constructor`, and `toString` can’t influence results.

Apply this rule to any “dictionary” object (e.g., `Record<string, ...>`) used for security-sensitive behavior or rendering decisions.

Example:
```ts
type IconSpec = { /* ... */ };
const BY_EXTENSION: Record<string, IconSpec> = {
  ts: { /* ... */ },
  json: { /* ... */ },
};

function lookupByExtension(ext: string): IconSpec | null {
  // ext may come from a user-controlled filename/path
  if (Object.hasOwn(BY_EXTENSION, ext)) {
    return BY_EXTENSION[ext];
  }
  return null; // safe default
}
```

Coding standard:
- Prefer `Object.hasOwn(map, key)` before reading `map[key]`.
- Otherwise fall back to a safe neutral default.
- Add tests for keys like `__proto__`, `constructor`, and `toString` where applicable.