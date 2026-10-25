---
title: Own-Property Safe Lookups
description: When you derive keys (extensions, filenames, paths) from user-controlled
  input to select behavior or presentation, use *own-property safe lookups* (or `Map`)
  and fail to a neutral default for unknown keys. This prevents inherited/prototype
  properties (e.g., `__proto__`, `constructor`, `toString`) from being treated as
  valid entries.
repository: CLINE/cline
label: Security
language: TSX
comments_count: 3
repository_stars: 70839
---

When you derive keys (extensions, filenames, paths) from user-controlled input to select behavior or presentation, use *own-property safe lookups* (or `Map`) and fail to a neutral default for unknown keys. This prevents inherited/prototype properties (e.g., `__proto__`, `constructor`, `toString`) from being treated as valid entries.

Apply it like this:

```ts
type IconSpec = { icon: unknown; className: string };
const BY_EXTENSION: Record<string, IconSpec> = {
  ts: { icon: /*...*/ null, className: "text-sky-600 dark:text-sky-400" },
  // ...
};

function baseName(path: string): string {
  return path.split(/[\\/]/).pop() ?? path;
}

export function safeSpecForPath(path: string): IconSpec {
  const name = baseName(path).toLowerCase();
  const ext = name.includes(".") ? (name.split(".").pop() ?? "").toLowerCase() : "";

  // own-property guard against prototype pollution/inherited keys
  if (Object.hasOwn(BY_EXTENSION, ext)) return BY_EXTENSION[ext];

  // neutral/fail-closed default
  return { icon: null, className: "text-muted-foreground" };
}
```

Additionally, for security-sensitive settings or permission changes, ensure the UI copy precisely distinguishes *what is allowed* (e.g., read vs sandboxed command write) and *where commands run* (background executor vs terminal), since ambiguity can lead users to unsafe assumptions.