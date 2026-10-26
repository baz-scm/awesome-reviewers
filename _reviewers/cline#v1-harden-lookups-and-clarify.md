---
title: Harden lookups and clarify
description: 'Apply this security standard to code paths driven by user-controlled
  strings (e.g., file paths/extensions) and to any security-related setting/UX:


  1) Harden object-key lookups'
repository: cline/cline#v1
label: Security
language: TSX
comments_count: 3
repository_stars: 70862
---

Apply this security standard to code paths driven by user-controlled strings (e.g., file paths/extensions) and to any security-related setting/UX:

1) Harden object-key lookups
- If you map a derived string (filename, extension, “language”, etc.) to an object/record, only accept *own* properties.
- Use `Object.hasOwn(map, key)` (or `Object.prototype.hasOwnProperty.call(map, key)`) before reading `map[key]`.
- Add a test for keys like `__proto__`, `constructor`, and `x.constructor` to ensure you fall back safely.

Example (safe lookup):
```ts
type IconSpec = { icon: unknown; className: string };
const BY_EXTENSION: Record<string, IconSpec> = {
  ts: { icon: 'Code', className: 'text-sky-600' },
};

function iconForPath(path: string): IconSpec {
  const name = path.split(/[\\/]/).pop() ?? path;
  const ext = name.includes('.') ? (name.split('.').pop() ?? '').toLowerCase() : '';

  if (Object.hasOwn(BY_EXTENSION, ext)) return BY_EXTENSION[ext];
  // neutral fallback
  return { icon: 'FileText', className: 'text-muted-foreground' };
}
```

2) Make security constraints unambiguous in UI
- If a setting changes authorization/sandbox behavior, the description must clearly distinguish what remains permitted (e.g., “read anywhere”) vs what is restricted (e.g., “write only within this project”).
- Call out platform-specific differences (e.g., Windows tool vs sandboxed command behavior).
- Clarify the execution context (e.g., background executor vs integrated terminal) when the UX could otherwise mislead users.

Together, these prevent prototype-chain edge cases from affecting security-relevant logic and ensure users understand the real authorization boundaries their settings enforce.