---
title: Own-Property Lookup Hardening
description: When indexing lookup tables with keys derived from untrusted input (e.g.,
  file paths/extensions/names), never rely on plain object property access alone.
  Use an own-property check (e.g., `Object.hasOwn`) or a `Map`, and provide a safe
  fallback icon/value.
repository: cline/cline#v11
label: Security
language: TSX
comments_count: 2
repository_stars: 70871
---

When indexing lookup tables with keys derived from untrusted input (e.g., file paths/extensions/names), never rely on plain object property access alone. Use an own-property check (e.g., `Object.hasOwn`) or a `Map`, and provide a safe fallback icon/value.

Why: inherited properties like `__proto__`, `constructor`, or `toString` can be reached via normal indexing. Own-property lookup prevents those prototype/inheritance properties from being treated as legitimate matches.

Apply like this:

```ts
type IconSpec = { icon: any; className: string };
const BY_EXTENSION: Record<string, IconSpec> = { ts: { icon: 'TS', className: '...' } };

function iconForPath(path: string): IconSpec {
  const name = path.split(/[\\/]/).pop() ?? path;
  const extension = name.includes('.')
    ? (name.split('.').pop() ?? '').toLowerCase()
    : '';

  // Harden against prototype/inherited keys
  if (Object.hasOwn(BY_EXTENSION, extension)) {
    return BY_EXTENSION[extension];
  }

  // Safe default
  return { icon: 'Neutral', className: 'text-muted-foreground' };
}
```

Team standard:
- Use `Object.hasOwn(table, key)` before returning `table[key]` for untrusted keys.
- Always include a neutral/safe fallback.
- Add tests covering `__proto__`, `constructor`, and `toString`-style keys (as demonstrated by the added tests).