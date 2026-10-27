---
title: Null-safe Location Handling
description: 'Always treat IR/AST location metadata and optional fields as nullable
  and identity-unstable:


  1) Guard and preserve `loc/start/end`

  - If a node/field may be missing (`loc == null`, `start/end === undefined`), don’t
  assume it exists.'
repository: facebook/react#b15
label: Null Handling
language: TypeScript
comments_count: 4
repository_stars: 251891
---

Always treat IR/AST location metadata and optional fields as nullable and identity-unstable:

1) Guard and preserve `loc/start/end`
- If a node/field may be missing (`loc == null`, `start/end === undefined`), don’t assume it exists.
- When creating/transformation-copying nodes, copy *all* available location information consistently (e.g., include `start/end` when the source has them).
- When recomputing locations, set them based on whatever nullable inputs you actually have (e.g., if `init` is `null`, derive the variable declarator `loc` from `id.loc` only).

Example pattern:
```ts
function applyLocFromSources(node: t.Node, sourceNodes: Map<any, any>): void {
  if (node.loc == null) return;
  const source = sourceNodes.get(node.loc);
  if (source == null) return;

  if (source.start === undefined) delete (node as any).start;
  else (node as any).start = source.start;

  if (source.end === undefined) delete (node as any).end;
  else (node as any).end = source.end;
}

function createVariableDeclarator(id: t.LVal, init?: t.Expression | null) {
  const node = t.variableDeclarator(id, init);
  if (id.loc) {
    // If init is null/without loc, fall back to id.loc.
    node.loc = {
      start: id.loc.start,
      end: init?.loc?.end ?? id.loc.end,
      filename: id.loc.filename,
      identifierName: undefined,
    };
  }
  return node;
}
```

2) Don’t key logic/maps off optional `loc.*` subfields
- Never rely on `loc.identifierName` (or similar) being present; it may be missing or non-unique.
- Use stable identifiers (e.g., an IR `IdentifierId`/`Identifier` object) as map keys instead of optional location-derived strings.

3) Align `??`/optional logic with real nullability
- If a condition uses `??` or checks that imply one side is non-nullable, ensure the RHS behavior matches the type system/actual runtime evaluation—otherwise you may silently ignore the RHS in null/undefined fixpoint logic.

If you apply these consistently, you avoid mismatched backend spans, missing source ranges, incorrect grouping by optional location fields, and subtle nullability-driven logic bugs.