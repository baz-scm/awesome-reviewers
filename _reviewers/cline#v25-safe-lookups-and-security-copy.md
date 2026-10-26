---
title: Safe Lookups And Security Copy
description: 'Apply two security-focused standards:


  1) Prevent prototype/inherited-property lookups in key-to-value tables

  - When mapping user- or filesystem-controlled strings (e.g., file paths, extensions,
  names) to icons/languages/config, do not rely on plain object indexing alone.'
repository: cline/cline#v25
label: Security
language: TSX
comments_count: 3
repository_stars: 70891
---

Apply two security-focused standards:

1) Prevent prototype/inherited-property lookups in key-to-value tables
- When mapping user- or filesystem-controlled strings (e.g., file paths, extensions, names) to icons/languages/config, do not rely on plain object indexing alone.
- Use `Object.hasOwn` (or prefer `Map`) so keys like `__proto__`, `constructor`, or `toString` can’t resolve to inherited properties.

Example (safe object-table lookup):
```ts
type Spec = { icon: unknown; className: string };
const BY_EXTENSION: Record<string, Spec> = {
  ts: { icon: 'FileCode2', className: 'text-sky-600' },
};

function specForPath(path: string): Spec {
  const name = path.split(/[\\/]/).pop() ?? path;
  const ext = name.includes('.') ? (name.split('.').pop() ?? '').toLowerCase() : '';

  // Own-property check prevents inherited-property abuse
  if (Object.hasOwn(BY_EXTENSION, ext)) return BY_EXTENSION[ext];

  // Neutral fallback
  return { icon: 'FileText', className: 'text-muted-foreground' };
}
```

2) Make security setting text precisely match enforced behavior
- If a setting changes the sandboxing boundary (read vs write/command execution), ensure the description states the distinction explicitly.
- Clarify execution context differences (e.g., what runs in the background executor vs the integrated terminal) and call out platform-specific ambiguity (e.g., Windows).

Practical rule of thumb:
- “What the app can still read” must be clearly separated from “what commands can modify,” and the UI copy must reflect where/how commands actually run when the setting is enabled.