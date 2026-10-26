---
title: Secure Lookup And Boundaries
description: When you map user-controlled inputs (paths, filenames, extensions) to
  configuration/behavior via JavaScript object literals, never rely on inherited properties.
  Always check ownership (e.g., `Object.hasOwn`) before using a lookup result, so
  keys like `__proto__`, `constructor`, and `toString` can’t change behavior.
repository: cline/cline#v13
label: Security
language: TSX
comments_count: 3
repository_stars: 70874
---

When you map user-controlled inputs (paths, filenames, extensions) to configuration/behavior via JavaScript object literals, never rely on inherited properties. Always check ownership (e.g., `Object.hasOwn`) before using a lookup result, so keys like `__proto__`, `constructor`, and `toString` can’t change behavior.

Also, for security-related settings, ensure the UI copy clearly distinguishes what’s allowed vs disallowed (e.g., read vs write/command effects) and clarifies execution context (e.g., background executor vs integrated terminal) to avoid operator misunderstanding.

Example (safe lookup):
```ts
type IconSpec = { icon: unknown; className: string };

const BY_EXTENSION: Record<string, IconSpec> = {
  ts: { icon: 'code', className: 'text-sky-600 dark:text-sky-400' },
};

export function iconSpecForPath(path: string): IconSpec {
  const name = path.split(/[\\/]/).pop() ?? path;
  const ext = name.toLowerCase().includes('.')
    ? (name.toLowerCase().split('.').pop() ?? '')
    : '';

  const key = ext;
  if (Object.hasOwn(BY_EXTENSION, key)) {
    return BY_EXTENSION[key];
  }

  // Neutral fallback: never allow inherited Object members
  return { icon: 'file', className: 'text-muted-foreground' };
}
```

Checklist:
- Use `Object.hasOwn(map, key)` (or a `Map` with `has()`) for lookups keyed by derived user input.
- Provide a neutral fallback for unknown keys.
- For security settings, write unambiguous copy that matches real sandbox permissions (read vs change) and runtime execution context.