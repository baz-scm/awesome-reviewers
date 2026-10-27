---
title: Actionable invariant diagnostics
description: When an error can occur (e.g., due to missing mappings/definitions or
  validation over new IR shapes), ensure failures are (1) prevented via complete definitions
  and (2) made actionable by preserving source-location context for diagnostics/suggestions.
repository: facebook/react#b9
label: Error Handling
language: TypeScript
comments_count: 2
repository_stars: 251891
---

When an error can occur (e.g., due to missing mappings/definitions or validation over new IR shapes), ensure failures are (1) prevented via complete definitions and (2) made actionable by preserving source-location context for diagnostics/suggestions.

Apply this in two checks:
1) Definition completeness (avoid opaque invariants)
- If you register an ID/shape/type for processing, you must also provide its corresponding definition/handler.
- Don’t rely on invariant-only failures to “work”; invariants that aren’t surfaced in the normal lint/diagnostics pipeline lead to silent or confusing compiler behavior.

Example pattern:
```ts
addObject(BUILTIN_SHAPES, ReanimatedSharedValueId, []); // ensure every registered shape id has a definition
```

2) Diagnostic context (enable targeted fixes)
- When adding new variants to validation/analysis models, carry `loc: SourceLocation` (or equivalent) so that any reported error can point to the exact code and optionally produce an automated `suggestion`.

Example pattern:
```ts
type Temporary =
  | { kind: 'Function'; dependencies: Set<Temporary>; loc: SourceLocation }
  | { kind: 'Aggregate'; dependencies: Set<InferredDependency>; loc: SourceLocation };
```

Net effect: errors fail loudly and usefully—no missing-definition surprises, and no “can’t locate the problem” situations that block precise guidance or auto-fixes.