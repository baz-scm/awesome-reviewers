---
title: Fail Loudly On Invariants
description: 'Make internal correctness checks explicit and actionable: when code
  depends on referenced definitions or invariants, validate them early and surface
  failures with context (ideally source locations) instead of letting an internal
  invariant crash or silently fail.'
repository: facebook/react#b10
label: Error Handling
language: TypeScript
comments_count: 3
repository_stars: 251894
---

Make internal correctness checks explicit and actionable: when code depends on referenced definitions or invariants, validate them early and surface failures with context (ideally source locations) instead of letting an internal invariant crash or silently fail.

Apply this as a standard:
- Validate referenced IDs/shapes/lookup keys exist before continuing (don’t allow “shape id defined, but no shape definition”).
- If correctness relies on an assumption, either (a) prove it via call-site validation, or (b) enforce it with `CompilerError.invariant(...)` that includes enough context to diagnose.
- When you produce diagnostics that can later drive automated fixes, carry `loc: SourceLocation` so suggestions can point to the user’s code.

Example pattern:
```ts
// Ensure referenced definitions exist
if (BUILTIN_SHAPES[id] === undefined) {
  throw CompilerError.invariant(
    `Missing shape definition for id: ${id}`,
  );
}

// Enforce assumptions explicitly
CompilerError.invariant(
  sourcesIds.every(id => cache.has(id)),
  'Unexpected sourceId added; expected only known sourceIds',
);

// Preserve location for actionable suggestions
type Aggregate = { kind: 'Aggregate'; dependencies: Set<InferredDependency>; loc: SourceLocation };
```