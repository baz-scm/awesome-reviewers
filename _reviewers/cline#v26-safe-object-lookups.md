---
title: Safe Object Lookups
description: When building lookup tables keyed by externally influenced strings (e.g.,
  file paths, extensions, filenames, folder names), do not rely on raw property access
  (`map[key]`) without guarding against prototype-inherited keys like `__proto__`,
  `constructor`, or `toString`. Use an own-property check so only explicitly defined
  keys are used.
repository: cline/cline#v26
label: Security
language: TSX
comments_count: 2
repository_stars: 70893
---

When building lookup tables keyed by externally influenced strings (e.g., file paths, extensions, filenames, folder names), do not rely on raw property access (`map[key]`) without guarding against prototype-inherited keys like `__proto__`, `constructor`, or `toString`. Use an own-property check so only explicitly defined keys are used.

Pattern to use:
```ts
type IconSpec = { icon: unknown; className: string };
const BY_EXTENSION: Record<string, IconSpec> = {
  ts: { icon: 'file', className: 'text-blue-500' },
};

export function iconForPath(path: string): IconSpec | null {
  const name = path.split(/[\\/]/).pop() ?? path;
  const ext = name.includes('.') ? (name.split('.').pop() ?? '').toLowerCase() : '';

  if (Object.hasOwn(BY_EXTENSION, ext)) return BY_EXTENSION[ext];
  return null; // or a neutral default
}
```

Apply this anywhere you map untrusted strings to behavior (icons, languages, handlers, routing, permissions) using plain objects. Add/keep tests for keys such as `__proto__` and `constructor` to ensure the neutral/default branch is taken.