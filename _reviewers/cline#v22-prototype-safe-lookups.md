---
title: Prototype-safe Lookups
description: 'When security-relevant behavior depends on user/externally-derived strings
  (file paths, extensions, names, etc.), treat those strings as untrusted and:'
repository: cline/cline#v22
label: Security
language: TSX
comments_count: 3
repository_stars: 70886
---

When security-relevant behavior depends on user/externally-derived strings (file paths, extensions, names, etc.), treat those strings as untrusted and:

1) Use prototype-safe lookup for maps
- If you index a plain object by a derived key (e.g., extension from a path), never rely on implicit property access that can hit the prototype chain.
- Only accept keys that are own-properties; otherwise fall back to a safe default.

Example:
```ts
type IconSpec = { icon: unknown; className: string };

const BY_EXTENSION: Record<string, IconSpec> = {
  ts: { icon: 'FileCode', className: 'text-sky-600' },
  // ...
};

function safeLookupByOwnProperty<T>(map: Record<string, T>, key: string, fallback: T): T {
  return Object.hasOwn(map, key) ? map[key] : fallback;
}

export function fileTypeSpec(path: string): IconSpec {
  const name = path.split(/[\\/]/).pop() ?? path;
  const ext = name.includes('.') ? (name.split('.').pop() ?? '').toLowerCase() : '';
  const FALLBACK: IconSpec = { icon: 'FileText', className: 'text-muted-foreground' };
  return safeLookupByOwnProperty(BY_EXTENSION, ext, FALLBACK);
}
```

2) Make security UI text match real permissions/execution
- For settings that change sandboxing or approval behavior, the description must precisely distinguish:
  - what operations can occur (e.g., file tools vs sandboxed command/file mutation),
  - where commands run (background executor vs integrated terminal), and
  - OS-specific behavior/limitations (e.g., Windows nuance).
- Ambiguous copy is a security issue because it can cause users to incorrectly trust what the system will or won’t allow.

Applying these rules prevents prototype-chain/key confusion bugs and reduces the risk of misunderstanding security controls.