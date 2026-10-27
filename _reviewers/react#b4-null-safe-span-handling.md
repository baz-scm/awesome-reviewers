---
title: Null-Safe Span Handling
description: 'When dealing with nullable/optional compiler/AST/IR metadata (especially
  `loc`/span fields), never assume required shape or fields exist.


  Apply these rules:'
repository: facebook/react#b4
label: Null Handling
language: TypeScript
comments_count: 3
repository_stars: 251885
---

When dealing with nullable/optional compiler/AST/IR metadata (especially `loc`/span fields), never assume required shape or fields exist.

Apply these rules:
1) Preserve span fields on copied nodes
- If downstream consumers rely on `node.start/end`, ensure node-creation/copying keeps those offsets when available.
- If source offsets are missing/undefined, delete the target properties rather than leaving stale/partial values.

```ts
const applySourceOffsets = (node: t.Node, sourceNodes: Map<any, {start?: number; end?: number}>) => {
  if (node.loc == null) return;
  const source = sourceNodes.get(node.loc);
  if (!source) return;

  if (source.start === undefined) delete (node as any).start;
  else (node as any).start = source.start;

  if (source.end === undefined) delete (node as any).end;
  else (node as any).end = source.end;
};
```

2) Guard/narrow optional metadata before use
- Use type guards/invariants so you never access fields that might be missing or of an unexpected shape.

```ts
if (!isNamedIdentifier(sourceMetadata.place)) {
  CompilerError.invariant(false, { reason: 'Expected named place in derivation entries' });
}
// safe to use: sourceMetadata.place.identifier.id
```

3) Don’t key caches/maps by optional `loc` subfields
- Avoid deriving keys from optional fields like `loc.identifierName` (which may be null/undefined and collapse unrelated entries).
- Prefer stable identifiers/types for `Map` keys; explicitly handle “missing metadata” by skipping, using a dedicated sentinel, or storing separate buckets keyed by the stable id.

This prevents null-reference crashes and avoids subtle mis-associations caused by absent/optional span/location data.