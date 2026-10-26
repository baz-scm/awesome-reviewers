---
title: Safe Own-Property Security
description: When behavior is selected from dynamic keys (paths/extensions/names)
  or from security-related settings copy, treat inputs as untrusted and ensure (1)
  map lookups are restricted to own-properties and (2) the security boundary is explicitly
  and unambiguously communicated.
repository: cline/cline?x=1
label: Security
language: TSX
comments_count: 3
repository_stars: 70861
---

When behavior is selected from dynamic keys (paths/extensions/names) or from security-related settings copy, treat inputs as untrusted and ensure (1) map lookups are restricted to own-properties and (2) the security boundary is explicitly and unambiguously communicated.

**1) Use own-property lookup for dynamic maps**
If you index an object with a derived key, prevent inherited/prototype keys like `__proto__`, `constructor`, or `toString` from being treated as valid. Use `Object.hasOwn` (or `Object.prototype.hasOwnProperty.call`) and fall back to a neutral/default.

```ts
type IconSpec = { icon: unknown; className: string };

const BY_EXTENSION: Record<string, IconSpec> = {
  ts: { icon: 'file', className: 'text-sky-600' },
  // ...
};

function iconSpecForPath(path: string): IconSpec {
  const name = path.split(/[\\/]/).pop() ?? path;
  const extension = name.includes('.') ? (name.split('.').pop() ?? '').toLowerCase() : '';

  // Own-property only: blocks __proto__/constructor/toString attacks.
  if (Object.hasOwn(BY_EXTENSION, extension)) return BY_EXTENSION[extension];

  return { icon: 'file', className: 'text-muted-foreground' }; // neutral default
}
```

Apply this pattern consistently anywhere you map dynamic strings to logic (icons, language IDs, highlighters, feature flags, etc.), especially when test coverage includes adversarial keys.

**2) Make security boundaries explicit in UI copy**
For security-related settings descriptions:
- Distinguish clearly between **read capability** and **command capability** (e.g., “can read anywhere” vs “commands can only modify within the project”).
- Clarify **where commands run** (e.g., background executor vs integrated terminal) and how that affects permissions/sandboxing.
- Avoid platform ambiguities (e.g., Windows file access vs sandboxed command access); one clarifying sentence is better than a broad claim.