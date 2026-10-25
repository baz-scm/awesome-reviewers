---
title: Safe Lookups And Security Copy
description: 'When security-relevant logic maps user-controlled strings (e.g., file
  paths, extensions, names) or security settings to behavior, apply two rules:


  1) Use own-property lookups for key→value mappings.'
repository: cline/CLINE
label: Security
language: TSX
comments_count: 3
repository_stars: 70839
---

When security-relevant logic maps user-controlled strings (e.g., file paths, extensions, names) or security settings to behavior, apply two rules:

1) Use own-property lookups for key→value mappings.
- Do not allow inherited/prototype properties to affect the outcome.
- Prefer `Object.hasOwn(table, key)` (or create the map with `Object.create(null)`) and always fall back to a safe default.

```ts
type IconSpec = { /* ... */ };
const BY_EXTENSION: Record<string, IconSpec> = { /* ... */ };

function safeLookup<K extends string>(table: Record<K, IconSpec>, key: string, fallback: IconSpec): IconSpec {
  return Object.hasOwn(table, key) ? table[key as K] : fallback;
}

// Example usage
const ext = (path.split(/[\\/]/).pop() ?? path).toLowerCase();
const icon = safeLookup(BY_EXTENSION, ext, /* neutral icon spec */ ({/*...*/} as IconSpec));
```

2) Make sandbox boundaries explicit in security-related UI text.
- Clearly distinguish capabilities (e.g., “commands can only change files in this project” vs “can still read files anywhere”).
- State execution context when relevant (e.g., whether actions run in a background executor vs an integrated terminal).

This prevents prototype-key confusion bugs and reduces the risk of users misunderstanding the true security guarantees of the feature.