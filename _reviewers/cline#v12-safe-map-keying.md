---
title: Safe Map Keying
description: 'When you derive behavior from user-controlled strings (e.g., file paths,
  names, extensions) or from security settings, treat keys and wording as security-sensitive:'
repository: cline/cline#v12
label: Security
language: TSX
comments_count: 3
repository_stars: 70872
---

When you derive behavior from user-controlled strings (e.g., file paths, names, extensions) or from security settings, treat keys and wording as security-sensitive:

1) Use own-property lookups for dictionary reads
- Prefer `Object.hasOwn(dict, key)` (or `Object.prototype.hasOwnProperty.call`) before using `dict[key]`.
- This prevents prototype-chain keys like `__proto__`, `constructor`, `toString`, etc. from being interpreted as valid entries.
- Fall back to a safe/neutral default when the key is not an own property.

Example (TypeScript):
```ts
type Spec = { value: string };
const BY_EXTENSION: Record<string, Spec> = {
  ts: { value: "TypeScript" },
  json: { value: "JSON" },
};

function safeLookupByExtension(path: string): Spec {
  const name = path.split(/[\\/]/).pop() ?? path;
  const ext = name.includes(".") ? (name.split(".").pop() ?? "").toLowerCase() : "";

  // SECURITY: only trust own properties of the map
  if (Object.hasOwn(BY_EXTENSION, ext)) return BY_EXTENSION[ext];

  // Safe neutral fallback
  return { value: "Unknown" };
}
```

2) Make security boundaries explicit in user-facing text
- If a setting changes what can be modified vs what can be read, state both explicitly (and note any OS-specific behavior).
- If execution context differs (e.g., background executor vs integrated terminal), mention it so users understand what the control actually enforces.

Apply this pattern anywhere you map untrusted inputs to actions or UI outcomes; it reduces the risk of prototype-chain confusion and prevents misleading security claims.