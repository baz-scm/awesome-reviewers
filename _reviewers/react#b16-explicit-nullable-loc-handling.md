---
title: Explicit nullable loc handling
description: 'When dealing with optional AST/HIR source ranges (`loc`, `start`, `end`,
  `identifierName`) treat them as nullable/possibly-missing everywhere: guard before
  dereferencing, narrow types, and only compute locations/cached entries when the
  required inputs exist. Also, never use optional `loc` strings (like `loc.identifierName`)
  as cache/map keys—if the value...'
repository: facebook/react#b16
label: Null Handling
language: TypeScript
comments_count: 5
repository_stars: 251891
---

When dealing with optional AST/HIR source ranges (`loc`, `start`, `end`, `identifierName`) treat them as nullable/possibly-missing everywhere: guard before dereferencing, narrow types, and only compute locations/cached entries when the required inputs exist. Also, never use optional `loc` strings (like `loc.identifierName`) as cache/map keys—if the value can be missing, different entries will collapse.

Practical rules:
1) Guard nullable fields before reads
- If `node.loc == null`, return early.
- If you depend on `id.loc` and `init?.loc`, only set `node.loc` when both exist.
- When cloning nodes, copy `start/end` (not only `loc`) if consumers expect span offsets.

2) Handle `null`/`undefined` intentionally
- For optional ranges, prefer explicit branching that assigns or deletes `node.start/node.end` based on whether the source has offsets.

3) Use stable keys for maps/caches
- Prefer `Map` keyed by a stable identifier/Place identity.
- Avoid `map.get(loc.identifierName)` patterns when `identifierName` may be absent.

Example pattern:
```ts
function applyOffsets(node: t.Node, sourceNodes: Map<any, any>) {
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

  // Only set declarator range when inputs exist.
  if (id.loc && init?.loc) {
    node.loc = {
      start: id.loc.start,
      end: init.loc.end,
      filename: id.loc.filename,
      identifierName: undefined,
    };
  }

  return node;
}
```
And for caching:
```ts
// Bad: identifierName may be missing and merges unrelated entries.
// const m = new Map<string, ...>();
// m.get(place.loc?.identifierName)

// Good: key by stable Place/ID.
const m = new Map<Place, Array<Place>>();
```