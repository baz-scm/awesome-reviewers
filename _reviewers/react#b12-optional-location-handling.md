---
title: Optional location handling
description: When dealing with `loc`/span metadata (especially in AST/HIR transforms
  and diagnostics), treat it as optional and nullable—never assume subfields are present,
  and never use missing `loc` data as identity.
repository: facebook/react#b12
label: Null Handling
language: TypeScript
comments_count: 4
repository_stars: 251896
---

When dealing with `loc`/span metadata (especially in AST/HIR transforms and diagnostics), treat it as optional and nullable—never assume subfields are present, and never use missing `loc` data as identity.

Apply this standard:
- **Null-guard reads:** check `node.loc == null` before using it.
- **Propagate consistently:** if a transform copies `loc`, also copy/derive `start`/`end` (or explicitly `delete node.start/end` when the source lacks them), so downstream span consumers behave the same across backends.
- **Reconstruct from partial data:** when building a new node’s range, support cases where only one side has location info.
  ```ts
  function setDeclaratorLoc(id: t.LVal, init: t.Expression | null | undefined, node: t.VariableDeclarator) {
    if (!id.loc) return;

    // If init exists and has loc, use id.start..init.end; otherwise fall back to id-only.
    if (init?.loc?.end !== undefined && id.loc.start !== undefined) {
      node.loc = {
        start: id.loc.start,
        end: init.loc.end,
        filename: id.loc.filename,
        identifierName: undefined,
      };
    } else {
      node.loc = {
        start: id.loc.start,
        end: id.loc.end,
        filename: id.loc.filename,
        identifierName: undefined,
      };
    }
  }
  ```
- **Don’t key by nullable `loc` subfields:** avoid using `loc.identifierName` (or similar) as a `Map` key unless you first ensure it’s always present and unique; otherwise distinct places may collapse to the same entry when the name is missing.
  - Prefer stable ids (e.g. `IdentifierId`, instruction ids) or the `Place`/object identity, or a tuple that can’t collapse due to missing `loc`.
- **Handle known loc-less forms explicitly:** if some AST nodes legitimately have no `loc` (e.g. hoisted `let x;`, certain `for-in/of` declarators), document them and decide whether to (a) widen the range conservatively, (b) leave ranges unset, or (c) add fixtures to track expected behavior.

This prevents null/undefined span fields from silently degrading ranges, and prevents incorrect diagnostics/analysis caused by identity being derived from missing location metadata.