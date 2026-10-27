---
title: Scope-Aware Naming
description: 'When generating or interpreting identifiers (e.g., JSX prop names or
  component/tag references), keep naming logic tightly scoped and documentation precise:'
repository: facebook/react#b11
label: Naming Conventions
language: TypeScript
comments_count: 2
repository_stars: 251894
---

When generating or interpreting identifiers (e.g., JSX prop names or component/tag references), keep naming logic tightly scoped and documentation precise:

- **Scope-aware deduplication:** If the generated identifiers live in a **fresh inner scope**, it’s safe to shadow outer bindings. Deduplicate only within the boundary where collisions can occur (e.g., per-element prop destructuring), rather than assuming you must avoid every outer-scope name.
- **Avoid over-scoping UID helpers:** Don’t switch to “global” UID generators that can cause unrelated behavioral/snapshot changes by mutating Babel/internal scope tracking. Prefer mechanisms that only affect the identifiers you actually need.
- **Register chosen names for later passes:** Ensure the names you select are added to whatever tracking structure later phases rely on (e.g., references collected for subsequent uid generation).
- **Make comments match the real input domain:** If parsing guarantees some forms can’t reach the code (e.g., invalid JSXIdentifiers are rejected earlier), word comments as “valid identifiers” (not all possible strings).

Example pattern for JSX-like prop sanitization:
```ts
// Deduplicate within the element’s generated destructuring scope
const seen = new Set<string>();

function choosePropKey(original: string): string {
  // Sanitize while ensuring collision avoidance is local to this scope
  const sanitized = /* e.g., camelCase for aria-label */ original;
  if (seen.has(sanitized)) throw new Error('collision');
  seen.add(sanitized);
  return sanitized;
}
```

And for tag classification comments:
```ts
// Only valid JSXIdentifiers reach here; invalid forms are rejected by the parser earlier.
if (tag.match(/^[a-z]/)) hostComponent();
else componentReference();
```