---
title: Null-safe location handling
description: 'When code depends on optional/null fields (e.g., AST `loc`, nested `loc.start/end`,
  `loc.identifierName`, optional `init`), enforce null safety and stable identity:'
repository: facebook/react#b8
label: Null Handling
language: TypeScript
comments_count: 5
repository_stars: 251889
---

When code depends on optional/null fields (e.g., AST `loc`, nested `loc.start/end`, `loc.identifierName`, optional `init`), enforce null safety and stable identity:

- Guard before reading: only access `node.loc.start/end` (or `init?.loc`) after checking the parent object isn’t null/undefined.
- Apply partial data correctly: if `init` is null, don’t read `init.loc`—derive location from `id.loc` only (or skip reconstruction when required fields are missing).
- Don’t key caches or identity off nullable metadata like `loc.identifierName` (it may be missing and cause unrelated entries to collide). Prefer stable IDs or composite keys; otherwise require the field to exist via a type guard.
- Use type guards/invariants for “expected structure” cases (e.g., `isNamedIdentifier(...)`) so invalid states fail early instead of continuing with incorrect assumptions.
- Avoid unsafe casts: after `null` checks/type guards, narrow types so you can remove `as`.

Example (safe reconstruction of a location with nullable init):
```ts
function createVariableDeclarator(id: t.LVal, init?: t.Expression | null): t.VariableDeclarator {
  const node = t.variableDeclarator(id, init);

  if (id.loc) {
    // Only use init.loc if init is actually present
    if (init?.loc) {
      node.loc = {
        start: id.loc.start,
        end: init.loc.end,
        filename: id.loc.filename,
        identifierName: undefined,
      };
    } else {
      // init is null: don't read init.loc; either omit loc or set only what you can
      // node.loc = { start: id.loc.start, end: ??? } // (avoid guessing end)
    }
  }

  return node;
}
```

Applying this standard prevents null-derived crashes, span/offset inconsistencies, and subtle cache/key collisions caused by missing `loc` subfields.