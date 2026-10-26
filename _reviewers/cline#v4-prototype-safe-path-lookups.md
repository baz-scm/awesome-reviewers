---
title: Prototype-Safe Path Lookups
description: When security-sensitive behavior depends on parsing a user-controlled
  string (e.g., file paths/extensions) and indexing into a lookup table, ensure the
  lookup only honors *own* keys. Avoid letting inherited/prototype properties like
  `__proto__`, `constructor`, or `toString` influence control flow.
repository: cline/cline#v4
label: Security
language: TSX
comments_count: 3
repository_stars: 70864
---

When security-sensitive behavior depends on parsing a user-controlled string (e.g., file paths/extensions) and indexing into a lookup table, ensure the lookup only honors *own* keys. Avoid letting inherited/prototype properties like `__proto__`, `constructor`, or `toString` influence control flow.

Apply this by using `Object.hasOwn` (or equivalent) instead of trusting plain property access, and add regression tests for dangerous keys. Also, if you expose security constraints via settings/UI, ensure copy precisely matches enforcement (e.g., clarify read-vs-write boundaries and which execution context is restricted).

Example pattern (prototype-safe):
```ts
type IconSpec = { icon: string; className: string };
const BY_EXTENSION: Record<string, IconSpec> = {
  ts: { icon: 'FileCode', className: 'text-sky-600' },
  json: { icon: 'Braces', className: 'text-amber-600' },
};

function specForPath(path: string): IconSpec | undefined {
  const name = path.split(/[\\/]/).pop() ?? path;
  const ext = name.includes('.') ? (name.split('.').pop() ?? '').toLowerCase() : '';

  // Only accept real keys
  return Object.hasOwn(BY_EXTENSION, ext) ? BY_EXTENSION[ext] : undefined;
}
```

Tests to include:
- `specForPath('file.__proto__')` (or similar)
- `specForPath('file.constructor')`
- `specForPath('file.toString')`

UI/security text checklist:
- Explicitly distinguish what is allowed (e.g., “read anywhere” vs “commands can only change files in this project”).
- Clarify execution context when it affects security expectations (e.g., background executor vs integrated terminal).