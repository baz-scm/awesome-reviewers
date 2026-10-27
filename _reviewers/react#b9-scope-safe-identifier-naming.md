---
title: Scope-Safe Identifier Naming
description: 'When code transforms source names into generated identifiers (variables/props/keys),
  enforce these rules:


  1) Preserve non-identifier property keys

  - If an input name is a valid JSX attribute name but not a valid JS identifier (e.g.
  `aria-label`), keep the original key in the call site and destructuring, using quoted
  keys.'
repository: facebook/react#b9
label: Naming Conventions
language: TypeScript
comments_count: 2
repository_stars: 251891
---

When code transforms source names into generated identifiers (variables/props/keys), enforce these rules:

1) Preserve non-identifier property keys
- If an input name is a valid JSX attribute name but not a valid JS identifier (e.g. `aria-label`), keep the original key in the call site and destructuring, using quoted keys.

2) Deterministically sanitize only for identifier positions
- Convert to an identifier using a predictable scheme (e.g. camelCasing), and fall back to a safe prefix if needed.

3) Make uniqueness decisions at the correct scope boundary
- Deduplicate/avoid collisions based on the scope where the generated identifiers actually live (e.g. the outlined function’s fresh scope), not on an incomplete or unrelated global set.
- If you need global uniqueness, use the program-context unique-id mechanism; otherwise keep dedup local to prevent unnecessary renames.

4) Don’t guess identifier types in internal metadata
- When collecting/processing “name” metadata, only accept named identifiers; enforce with invariants rather than continuing with missing/invalid name data.

Example pattern:

```ts
function isHyphenatedJsxProp(originalName: string): boolean {
  return (
    !isValidIdentifier(originalName) && /^[a-zA-Z_][\w.-]*$/.test(originalName)
  );
}

function sanitizeToIdentifier(name: string): string {
  if (isValidIdentifier(name)) return name;
  let base = name.replace(/[^a-zA-Z0-9$_]+(.)?/g, (_, c) => (c ? c.toUpperCase() : ''));
  if (!isValidIdentifier(base)) base = `_${base}`;
  return base;
}
```

Apply this whenever generating/destructuring identifiers from external names, and ensure your collision avoidance strategy matches the actual scope of the generated bindings.