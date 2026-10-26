---
title: Secure Lookup And Messaging
description: 'When code turns user-influenced strings (paths, filenames, extensions)
  or security settings into behavior or UI claims, treat both as security-sensitive:'
repository: cline/cline#v10
label: Security
language: TSX
comments_count: 3
repository_stars: 70869
---

When code turns user-influenced strings (paths, filenames, extensions) or security settings into behavior or UI claims, treat both as security-sensitive:

1) Prototype-safe dictionary lookups
- For any mapping like `BY_EXTENSION[name]` / `BY_NAME[filename]` / `EXTENSION_LANGUAGES[ext]`, ensure lookups do not fall back to inherited Object properties.
- Prefer either:
  - Use `Object.hasOwn(table, key)` before indexing, or
  - Create tables with a null prototype: `Object.create(null)`.
- Add tests that cover keys such as `__proto__`, `constructor`, and `toString`.

Example pattern (TypeScript):
```ts
type Spec = { icon: unknown; className: string };
const BY_EXTENSION: Record<string, Spec> = {/* ... */};

export function languageForPath(path: string): string {
  const name = path.split(/[\\/]/).pop() ?? path;
  const ext = name.includes(".") ? (name.split(".").pop() ?? "").toLowerCase() : "";

  // Prevent inherited-prototype surprises
  return Object.hasOwn(BY_EXTENSION, ext) ? (BY_EXTENSION as any)[ext] : ext;
}
```

2) Explicit permission boundaries in security-sensitive UI
- If a setting changes authorization/sandboxing, ensure copy clearly distinguishes what remains allowed (e.g., read via file tools) vs what is restricted (e.g., write/commands), especially for platform-specific behavior.
- Also clarify execution context when relevant (e.g., “background executor” vs “integrated terminal”).

Practical checklist
- [ ] Any path/extension-to-behavior mapping uses an own-property check (or null-prototype tables).
- [ ] Tests cover prototype-chain keys.
- [ ] Security setting text explicitly states read vs command/write permissions and where commands run.