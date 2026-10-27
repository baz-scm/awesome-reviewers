---
title: Stable null-safe handling
description: 'When dealing with nullable/optional values (especially source locations,
  spans, and diagnostic metadata), keep behavior explicit and stable:


  1) Never key correctness off optional subfields'
repository: facebook/react#b10
label: Null Handling
language: TypeScript
comments_count: 4
repository_stars: 251894
---

When dealing with nullable/optional values (especially source locations, spans, and diagnostic metadata), keep behavior explicit and stable:

1) Never key correctness off optional subfields
- Don’t use `loc.*` sub-properties (e.g. `loc.identifierName`) as map keys or identifiers if they can be missing/undefined.
- Prefer stable domain keys (e.g., `IdentifierId` / `Identifier`) and only store optional metadata as values.

2) Treat `start`/`end` (and other span offsets) as first-class data
- If a backend or transformer copies `loc` but drops `start`/`end`, span consumers may misbehave.
- Either consistently copy offsets (`start`/`end`) from the original node or explicitly remove them when unknown; don’t leave partially populated nodes.

3) After null checks, rely on type narrowing (avoid `as`)
- Pattern: `if (x != null) { use x }`.
- Don’t keep using `as` to “force” null-safety when the compiler can narrow.

4) Validate null-short-circuit logic
- For expressions like `a ?? b`, confirm which side is nullable and what the operator guarantees; don’t assume both sides behave the same.

Example (map key and null-safe narrowing):
```ts
// Prefer stable identifiers, not optional loc fields.
const placesById = new Map<IdentifierId, Place[]>();
const id = someIdentifier.identifier;
placesById.get(id)?.push(place);

// Span offsets: be explicit about undefined.
function applyOffsets(node: {start?: number; end?: number}, source: {start?: number; end?: number}) {
  if (source.start === undefined) delete node.start;
  else node.start = source.start;
  if (source.end === undefined) delete node.end;
  else node.end = source.end;
}

// Type narrowing instead of casts.
if (lvalue != null) {
  use(lvalue); // no `as` needed
}
```