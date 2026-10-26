---
title: Secure map lookups
description: 'When converting dynamic strings (file paths, extensions, names) into
  results via plain object lookup tables, treat keys as untrusted: only accept *own*
  properties and provide a safe default. Also, for security-related settings, ensure
  the UI copy precisely states the authorization boundary (e.g., read vs write) and
  the real execution context.'
repository: cline/cline#v7
label: Security
language: TSX
comments_count: 3
repository_stars: 70865
---

When converting dynamic strings (file paths, extensions, names) into results via plain object lookup tables, treat keys as untrusted: only accept *own* properties and provide a safe default. Also, for security-related settings, ensure the UI copy precisely states the authorization boundary (e.g., read vs write) and the real execution context.

**1) Harden string→object lookups**
- Use `Object.hasOwn(map, key)` (or an equivalent own-property check) instead of `map[key]`.
- If the key is not an own property, return a neutral fallback (do not allow `__proto__`, `constructor`, `toString`, etc. to influence behavior).

```ts
type IconSpec = { icon: unknown; className: string };
const BY_EXTENSION: Record<string, IconSpec> = {
  ts: { icon: {}, className: "text-sky-600" },
};
const NEUTRAL: IconSpec = { icon: {}, className: "text-muted-foreground" };

function extFromPath(path: string): string {
  const name = path.split(/[\\/]/).pop() ?? path;
  const parts = name.split(".");
  return parts.length > 1 ? parts.pop()!.toLowerCase() : "";
}

export function iconForPath(path: string): IconSpec {
  const ext = extFromPath(path);
  return (ext && Object.hasOwn(BY_EXTENSION, ext)) ? BY_EXTENSION[ext] : NEUTRAL;
}
```

**2) Make security setting copy unambiguous**
- Explicitly distinguish what is allowed in each mode (e.g., “can read files anywhere” vs “can only modify files in this project”).
- If enforcement differs by platform (Windows) or by executor surface (background command vs integrated terminal), mention that difference in one sentence.

Applying both prevents prototype-chain key attacks/misclassification and reduces security misunderstandings that can lead to unsafe user expectations.