---
title: Nullable Metadata Safety
description: 'When code depends on AST/span/metadata fields that are optional (`loc`,
  `loc.start/end`, `loc.identifierName`, `init?.loc`, etc.), treat them as unreliable:'
repository: facebook/react#b2
label: Null Handling
language: TypeScript
comments_count: 5
repository_stars: 251882
---

When code depends on AST/span/metadata fields that are optional (`loc`, `loc.start/end`, `loc.identifierName`, `init?.loc`, etc.), treat them as unreliable:

- **Guard every nullable read** before using it.
- **Use intentional fallbacks**: if only part of the location is available (e.g., `id.loc` but `init` is null), reconstruct location from what exists; if offsets are unavailable, don’t silently assume defaults—either omit them or delete previously-set fields.
- **Never use nullable location fields as identity keys.** If a `loc` subfield (like `identifierName`) can be missing, don’t map by it—map by stable IDs (e.g., declaration/identifier IDs) or represent “unknown” explicitly.
- **Refine null checks to keep types safe** (avoid `as` by narrowing via `if (x != null)` / optional chaining + guards).
- **Filter “off”/non-applicable entries rather than short-circuiting incorrectly** so optional states don’t incorrectly flip entire results.

Example pattern (reconstructing span offsets safely):
```ts
function applySourceOffsets(node: { loc?: { start?: any; end?: any } | null; start?: any; end?: any }, source: { start?: any; end?: any } | undefined) {
  if (node.loc == null || source == null) return;
  if (source.start === undefined) delete node.start;
  else node.start = source.start;

  if (source.end === undefined) delete node.end;
  else node.end = source.end;
}

function createVariableDeclarator(id: { loc?: any }, init: { loc?: any } | null) {
  const node = {/* ... */};
  if (id.loc) {
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

Adopting this prevents null reference errors, avoids inconsistent span behavior across components, and stops missing `loc` data from corrupting caches/keys.