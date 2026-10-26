---
title: Prototype-Safe Lookups
description: For any security-relevant feature that maps untrusted dynamic strings
  (paths, filenames, extensions) to configuration/data (icons, languages, policies),
  use prototype-safe lookups and make permission boundaries explicit in the UI.
repository: cline/cline#v16
label: Security
language: TSX
comments_count: 3
repository_stars: 70882
---

For any security-relevant feature that maps untrusted dynamic strings (paths, filenames, extensions) to configuration/data (icons, languages, policies), use prototype-safe lookups and make permission boundaries explicit in the UI.

1) Prototype-safe mapping for untrusted keys
- When doing `table[key]`, prefer `Object.hasOwn(table, key)` (or `Object.prototype.hasOwnProperty.call`) before returning a mapped value.
- If the key is not an own-property, fall back to a neutral/default value.
- Add tests covering crafted keys like `__proto__`, `constructor`, and `toString`.

Example:
```ts
type Spec = { value: string };
const TABLE: Record<string, Spec> = {
  ts: { value: "typescript" },
};

function safeLookup(table: Record<string, Spec>, key: string, fallback: Spec): Spec {
  return Object.hasOwn(table, key) ? table[key] : fallback;
}

function specForPath(path: string) {
  const name = path.split(/[\\/]/).pop() ?? path;
  const ext = name.includes(".") ? name.split(".").pop()!.toLowerCase() : "";
  return safeLookup(TABLE, ext, { value: "unknown" });
}
```

2) Security UX: clarify boundaries and execution context
- In user-facing security settings, explicitly distinguish:
  - Read access vs write/command execution scope (e.g., “commands can only change files in this project”).
  - Where commands run when enabled (e.g., background executor vs integrated terminal), especially if the UI implies a different behavior.
- Ensure copy is unambiguous across platforms (e.g., Windows sandboxing differences).