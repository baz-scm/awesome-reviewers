---
title: Safe Lookup For Security
description: 'When deriving behavior from untrusted strings (e.g., paths, filenames,
  extensions), treat dictionary lookups as security-sensitive.


  Apply these rules:'
repository: cline/cline#v19
label: Security
language: TSX
comments_count: 3
repository_stars: 70885
---

When deriving behavior from untrusted strings (e.g., paths, filenames, extensions), treat dictionary lookups as security-sensitive.

Apply these rules:

1) Prevent prototype-chain key injection
- If you use plain objects as lookup tables, only accept *own* properties.
- Use `Object.hasOwn(...)` (or prefer `Map`) and fall back to a safe default when there’s no own match.

Example (pattern):
```ts
type Spec = { value: string; className: string };
const BY_EXTENSION: Record<string, Spec> = {
  ts: { value: "ts", className: "text-sky-600" },
  json: { value: "json", className: "text-amber-600" },
};

export function specForPath(path: string): Spec {
  const name = path.split(/[\\/]/).pop() ?? path;
  const ext = name.includes(".") ? (name.split(".").pop() ?? "").toLowerCase() : "";

  if (Object.hasOwn(BY_EXTENSION, ext)) return BY_EXTENSION[ext];
  return { value: "", className: "text-muted-foreground" }; // safe neutral fallback
}
```
- Add tests for adversarial keys like `constructor`, `__proto__`, and `toString`.

2) Make security boundaries explicit in security-related UI
- Avoid ambiguous wording around permissions. Clearly distinguish what can be read vs what can be changed (and how platform differences apply).
- If a setting changes execution context (e.g., background executor vs integrated terminal), state that in one sentence so operators understand the real behavior.

Together, these practices reduce both technical exploitation risk (prototype-chain lookup injection) and human configuration risk (misunderstanding sandbox/authorization behavior).