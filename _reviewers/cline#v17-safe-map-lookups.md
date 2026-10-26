---
title: Safe Map Lookups
description: 'When you derive keys from paths/user input (extensions, filenames, identifiers)
  to select behavior from an object/record, treat the mapping as security-sensitive:'
repository: cline/cline#v17
label: Security
language: TSX
comments_count: 4
repository_stars: 70883
---

When you derive keys from paths/user input (extensions, filenames, identifiers) to select behavior from an object/record, treat the mapping as security-sensitive:

1) Use own-property lookups (avoid inherited keys)
- If you store mappings like `Record<string, ...>`, guard with `Object.hasOwn(map, key)` (or equivalent) before using the value.
- This prevents prototype/inherited properties such as `__proto__`, `constructor`, or `toString` from being treated as valid entries.

2) Normalize identifiers consistently end-to-end
- If you trim/normalize (e.g., menu paths, command names, file paths), apply the same normalization in every stage that interprets the identifier (registration/inspection/execution). Divergence can lead to security checks and execution targeting different strings.

3) Match security UI text to enforced boundaries
- When permissions/sandboxing differ between “read” and “command execution,” make that distinction explicit in the UI, including execution context where relevant.

Example (prototype-safe + consistent normalization):
```ts
type IconSpec = { icon: unknown; className: string };
const BY_EXTENSION: Record<string, IconSpec> = { ts: { icon: 'file', className: 'text-sky' } };

function extensionForPath(path: string): string {
  const name = path.split(/[\\/]/).pop() ?? path;
  const rawExt = name.includes('.') ? (name.split('.').pop() ?? '') : '';
  return rawExt.toLowerCase().trim(); // apply the same normalization everywhere you use the key
}

export function iconSpecForPath(path: string): IconSpec {
  const ext = extensionForPath(path);
  if (Object.hasOwn(BY_EXTENSION, ext)) return BY_EXTENSION[ext];
  return { icon: 'file', className: 'text-muted-foreground' }; // neutral fallback
}
```

Add regression tests for “poison” keys (e.g., `__proto__`, `constructor`) to ensure the lookup never returns mapped values for inherited properties.