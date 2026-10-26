---
title: Fail Loudly With Context
description: When code relies on internal compiler invariants or on complete metadata
  (e.g., shape IDs), treat violations as explicit, user-actionable errors rather than
  silent failures.
repository: facebook/react#b3
label: Error Handling
language: TypeScript
comments_count: 4
repository_stars: 251883
---

When code relies on internal compiler invariants or on complete metadata (e.g., shape IDs), treat violations as explicit, user-actionable errors rather than silent failures.

Apply these rules:
1) Ensure completeness of referenced definitions
- If you add/introduce an identifier (shapeId/object id/type), also add the corresponding definition/registration so property resolution can’t hit an unhandled invariant.
- Example pattern:
  ```ts
  // Ensure every referenced shape id is registered with BUILTIN_SHAPES
  addObject(BUILTIN_SHAPES, ReanimatedSharedValueId, []);
  ```

2) Convert “should never happen” assumptions into explicit compiler errors
- Guard assumptions that would otherwise lead to confusing downstream behavior with `CompilerError.invariant`, including a clear `reason`.
  ```ts
  CompilerError.invariant(isNamedIdentifier(sourceMetadata.place), {
    reason: 'Compiler internal error: expected derivation entries to reference named variables',
  });
  ```

3) Make diagnostics actionable
- When building validation/analysis structures that later produce suggestions or automated fixes, include `loc: SourceLocation` (or equivalent) so errors can point to the user’s code (e.g., manual dependency arrays) and suggestions can be precise.

4) Choose safely between “assert” and “assume”
- If you can prove a condition is always true (e.g., via prior checks), you may keep the invariant as an assertion; otherwise, keep the runtime check to prevent silent compiler failures and to make debugging faster.