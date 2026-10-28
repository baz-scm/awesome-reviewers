---
title: Guard against prototype pollution lookups
description: When indexing a plain-object lookup table (e.g., maps keyed by file extension,
  filename, or folder name) with a string derived from user input or file paths, never
  rely on plain bracket access like `table[key]`. Such keys can accidentally match
  inherited `Object.prototype` members (`constructor`, `__proto__`, `toString`, `hasOwnProperty`,
  etc.), causing...
repository: "cline/cline\t"
label: Security
language: TSX
comments_count: 2
repository_stars: 70947
---

When indexing a plain-object lookup table (e.g., maps keyed by file extension, filename, or folder name) with a string derived from user input or file paths, never rely on plain bracket access like `table[key]`. Such keys can accidentally match inherited `Object.prototype` members (`constructor`, `__proto__`, `toString`, `hasOwnProperty`, etc.), causing incorrect fallbacks or leaking internal object references instead of returning "not found". Always verify the key is an own property before reading it, e.g.:

```ts
function lookup(table: Record<string, IconSpec>, key: string): IconSpec | undefined {
  return Object.hasOwn(table, key) ? table[key] : undefined;
}
```

Apply this pattern consistently to any object used as a dictionary with external or derived keys, and add regression tests for adversarial keys such as `"constructor"`, `"__proto__"`, and `"toString"` to confirm they resolve to the default/neutral behavior rather than an inherited value.