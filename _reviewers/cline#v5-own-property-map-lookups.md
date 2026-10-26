---
title: Own-Property Map Lookups
description: When mapping untrusted strings (e.g., paths, filenames, extensions) to
  behavior/config via plain objects, never rely on prototype-chain properties. Only
  use the mapping when the key is an *own* property; otherwise fall back to a safe
  default.
repository: cline/cline#v5
label: Security
language: TSX
comments_count: 2
repository_stars: 70864
---

When mapping untrusted strings (e.g., paths, filenames, extensions) to behavior/config via plain objects, never rely on prototype-chain properties. Only use the mapping when the key is an *own* property; otherwise fall back to a safe default.

Apply this to any code like icon/type/language selection:

```ts
type Spec = { value: string };
const BY_EXT: Record<string, Spec> = {
  ts: { value: "typescript" },
};

function safeLookup(ext: string): Spec {
  // Prevent prototype-chain keys like "__proto__" / "constructor" / "toString".
  if (Object.hasOwn(BY_EXT, ext)) return BY_EXT[ext];
  return { value: "unknown" };
}

export function languageForPath(path: string): string {
  const name = path.split(/[\\/]/).pop() ?? path;
  const ext = name.includes(".") ? (name.split(".").pop() ?? "").toLowerCase() : "";
  return Object.hasOwn(BY_EXT, ext) ? BY_EXT[ext].value : ext;
}
```

Checklist:
- For `Record<string, ...>` maps driven by input, gate access with `Object.hasOwn(map, key)` (or equivalent).
- Fall back to a neutral/default spec when the key is not an own property.
- Add tests using malicious keys (e.g., `"__proto__"`, `"constructor"`, `"toString"`) to ensure safe defaults are returned.