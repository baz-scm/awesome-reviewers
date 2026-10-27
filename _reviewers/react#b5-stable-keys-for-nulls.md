---
title: Stable Keys for Nulls
description: 'Null/optional metadata must never silently change program behavior.
  Apply these rules:


  1) Validate nullable fields before use

  - If a field like `node.loc`, `loc.identifierName`, or `start/end` can be missing,
  either:'
repository: facebook/react#b5
label: Null Handling
language: TypeScript
comments_count: 4
repository_stars: 251886
---

Null/optional metadata must never silently change program behavior. Apply these rules:

1) Validate nullable fields before use
- If a field like `node.loc`, `loc.identifierName`, or `start/end` can be missing, either:
  - return early, or
  - use an invariant that the value is in the expected shape.

2) Use stable identifiers for maps/caches
- Don’t key caches/maps using optional `loc.*` strings that may be missing (or may differ only because of source formatting).
- Instead, key by stable IDs (e.g., `IdentifierId`, instruction IDs) or other non-null internal handles.

3) Preserve or normalize required location offsets when transforming nodes
- When creating new AST/HIR nodes from originals, copy required offset fields (`start`/`end`) from the original node (or explicitly delete them if unavailable) so downstream span consumers behave consistently.

4) Prefer filtering non-applicable entries over control-flow shortcuts
- When a collection includes “off/ignored” entries, filter them into a new list/set rather than relying on early-return boolean logic that can hide additional meaningful details.

Example patterns:
```ts
// 1) Fail-fast on unexpected null/shape
CompilerError.invariant(isNamedIdentifier(place), {
  reason: 'Expected named identifier',
  loc: place?.loc,
  description: null,
  suggestions: null,
});

// 2) Stable cache key: avoid loc.identifierName
// BAD: const key = fnNode.loc?.identifierName;
// GOOD: const key = derivedVar.identifier.id;

// 3) Preserve offsets when cloning nodes
function applyOffsets(newNode: t.Node, original: t.Node) {
  newNode.start = original.start;
  newNode.end = original.end;
}

// 4) Filter out off/ignored details instead of boolean early exit
const visibleDetails = error.details.filter(d => d.severity !== ErrorSeverity.Off);
```