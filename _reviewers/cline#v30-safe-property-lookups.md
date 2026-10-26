---
title: Safe Property Lookups
description: When you map untrusted strings (paths, extensions, identifiers, plugin-provided
  keys) to security- or behavior-relevant outcomes, only accept *own* keys from your
  lookup tables.
repository: cline/cline#v30
label: Security
language: TSX
comments_count: 4
repository_stars: 70894
---

When you map untrusted strings (paths, extensions, identifiers, plugin-provided keys) to security- or behavior-relevant outcomes, only accept *own* keys from your lookup tables.

Practical standard:
- Use `Object.hasOwn(table, key)` (or an equivalent “own-property only” check) before using `table[key]`.
- Add regression tests using adversarial inputs like `"__proto__"`, `"constructor"`, and `"toString"`.
- Keep normalization consistent end-to-end for identifiers that affect registration/inspection/execution (e.g., trim paths/names in the same way everywhere).
- For security boundary features (read vs command permissions, sandboxing, execution context), make the UI text unambiguous about what is allowed and where commands run.

Example (own-property guard):
```ts
type IconSpec = { /* ... */ };
const BY_EXTENSION: Record<string, IconSpec> = { ts: /* ... */ };
const NEUTRAL: IconSpec = { /* ... */ };

export function specForExtension(ext: string): IconSpec {
  const key = ext.toLowerCase();
  return Object.hasOwn(BY_EXTENSION, key) ? BY_EXTENSION[key] : NEUTRAL;
}
```

This prevents prototype/inherited-property abuse from turning attacker-controlled keys into unexpected behavior, and it pairs with consistent identifier normalization to avoid security-relevant mismatches.