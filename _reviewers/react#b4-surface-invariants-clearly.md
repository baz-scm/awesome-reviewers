---
title: Surface Invariants Clearly
description: When adding compiler/validator logic, don’t let failure conditions remain
  implicit or silently reported. Convert “should never happen” assumptions and validation
  failures into either (1) corrected generated code that avoids the invalid state,
  or (2) diagnostics/invariants that are accurate, consistent, and context-rich.
repository: facebook/react#b4
label: Error Handling
language: TypeScript
comments_count: 5
repository_stars: 251885
---

When adding compiler/validator logic, don’t let failure conditions remain implicit or silently reported. Convert “should never happen” assumptions and validation failures into either (1) corrected generated code that avoids the invalid state, or (2) diagnostics/invariants that are accurate, consistent, and context-rich.

Practical rules:
- Replace invalid internal forms instead of relying on generic TODO/errors (e.g., if generated AST can’t legally appear inside a JS SequenceExpression, rewrite it to a valid form such as converting declarations to assignments).
- If you remove a defensive branch because the invariant is guaranteed by construction, enforce that guarantee with an invariant/assert at the boundary (and keep it documented in the error message).
- Ensure invariants are actually surfaced to users/tooling. If eslint won’t report them, make the compiler diagnostics explicit (category/message/loc) so failures aren’t “silent”.
- Keep invariant/diagnostic “reason” text consistent with the code’s expanded behavior (e.g., when supporting additional effect kinds, update the invariant message so it mentions the actual kind(s) expected).
- When diagnostics may become conditional (to avoid false positives), gate the error emission using precise checks (e.g., inspect the relevant argument/value shape before reporting).

Example pattern:
```ts
// Boundary assertion for an assumption we’re relying on.
CompilerError.invariant(
  initialized.has(effect.into.identifier.id) || effect.kind === 'Capture',
  {
    reason: `Expected destination value to already be initialized within this instruction for ${effect.kind} effect`,
  },
);

// If validation should be conditional, only emit when truly invalid.
if (blockIsUnconditional) {
  const arg0 = instr.value.args[0];
  if (arg0.kind === 'Identifier' && /* primitive + non-reactive checks */) {
    // allow
  } else {
    pushDiagnostic(/* include loc + actionable description */);
  }
}
```