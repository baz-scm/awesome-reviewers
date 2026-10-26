---
title: Harden Untrusted Lookups
description: When you build security- or safety-relevant behavior from external strings
  (file paths, extensions, filenames, UI settings, keyboard events), treat keys as
  untrusted and ensure you only accept *own* properties, not inherited prototype values.
  Also make authorization/sandbox boundaries explicit in UI text and gate sensitive
  global actions during modal flows.
repository: cline/cline#v21
label: Security
language: TSX
comments_count: 4
repository_stars: 70886
---

When you build security- or safety-relevant behavior from external strings (file paths, extensions, filenames, UI settings, keyboard events), treat keys as untrusted and ensure you only accept *own* properties, not inherited prototype values. Also make authorization/sandbox boundaries explicit in UI text and gate sensitive global actions during modal flows.

**Apply this rule**
1) **Use own-property checks for lookup tables**
- If you do `table[key]`, an attacker can sometimes influence behavior via `__proto__`, `constructor`, etc.
- Use `Object.hasOwn(table, key)` and fall back to a neutral/default mapping.

```ts
type Spec = { icon: unknown; className: string };
const BY_EXTENSION: Record<string, Spec> = { ts: { /* ... */ } };

export function safeLookup(table: Record<string, Spec>, key: string): Spec {
  const normalized = key.toLowerCase();
  return Object.hasOwn(table, normalized)
    ? table[normalized]
    : ({ icon: null, className: "text-muted-foreground" } as Spec);
}
```

2) **Make sandbox/authorization semantics explicit**
- If tools (read) and commands (write) differ due to sandboxing/enforcement, reflect that difference clearly in setting descriptions (including executor vs terminal behavior when relevant).

3) **Gate security-relevant global handlers during sensitive states**
- When recording or in a modal “capture” interaction, suspend or ignore global shortcuts/actions until the flow completes; ensure additional event propagation is stopped as needed.

This prevents prototype/inherited-property edge cases from altering mapping behavior, reduces user confusion about what’s authorized, and avoids unintended triggering of sensitive actions.