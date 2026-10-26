---
title: Prototype-Safe Maps
description: Treat any user- or workspace-derived strings (paths, filenames, extensions)
  as untrusted, and ensure security-sensitive mappings and UI copy can’t be tricked.
repository: cline/cline#v8
label: Security
language: TSX
comments_count: 3
repository_stars: 70867
---

Treat any user- or workspace-derived strings (paths, filenames, extensions) as untrusted, and ensure security-sensitive mappings and UI copy can’t be tricked.

**Implementation rule (prototype-safe lookups):** when indexing “dictionary” tables (maps of extensions → metadata, names → icons, etc.), only accept *own* properties. Use `Object.hasOwn` (or `Object.prototype.hasOwnProperty.call`) instead of direct property access that can be affected by inherited keys like `__proto__`, `constructor`, or `toString`.

```ts
type Entry = { value: string };
const TABLE: Record<string, Entry> = { js: { value: "JS" } };

function lookup(table: Record<string, Entry>, key: string): Entry | undefined {
  // key is derived from untrusted input (e.g., file path/extension)
  return Object.hasOwn(table, key) ? table[key] : undefined;
}

// Example usage
const ext = "__proto__"; // malicious
const entry = lookup(TABLE, ext);
// entry is undefined (falls back to neutral handling)
```

**Security UI rule (permission boundary clarity):** for settings that change sandboxing/approval behavior, make the enforced boundaries explicit (e.g., what’s allowed to *read* vs what’s allowed to *modify/write*; and whether commands run in a background executor vs an integrated terminal). Ambiguous wording can lead users to assume stronger guarantees than are actually enforced.

Apply both rules anywhere the system:
- maps paths/extensions/names to behavior or presentation,
- restricts filesystem access for commands vs tools,
- or exposes those restrictions through user-facing settings text.