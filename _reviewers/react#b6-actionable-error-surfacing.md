---
title: Actionable Error Surfacing
description: 'When adding/adjusting compiler validation logic, ensure failures don’t
  become unreported invariants or silent misbehavior. Concretely:


  - Surface user-impacting failures as diagnostics (or equivalent reported errors)
  with a precise `loc`.'
repository: facebook/react#b6
label: Error Handling
language: TypeScript
comments_count: 5
repository_stars: 251888
---

When adding/adjusting compiler validation logic, ensure failures don’t become unreported invariants or silent misbehavior. Concretely:

- Surface user-impacting failures as diagnostics (or equivalent reported errors) with a precise `loc`.
- Preserve source metadata needed to build actionable “suggestion” fixes after IR/AST transformations.
- Treat internal invariants intentionally: either prove preconditions earlier (so they truly can’t happen) or assert with a clear `CompilerError.invariant(...)` reason; don’t rely on assumptions that may be violated by missing registrations/config.
- Avoid blanket diagnostics when semantic inspection can narrow the failure condition (e.g., inspect call arguments / reactivity before reporting).

Example pattern (diagnostic + loc + guarded emission):
```ts
if (unconditionalBlocks.has(block.id)) {
  const arg = instr.value.args[0];
  const allow =
    arg?.kind === 'Identifier' &&
    !arg.reactive &&
    isPrimitiveSetArg(arg, fn);

  if (!allow) {
    errors.pushDiagnostic(
      CompilerDiagnostic.create({
        category: ErrorCategory.RenderSetState,
        reason: 'Calling setState during render may trigger an infinite loop',
        description: 'Calling setState during render will trigger another render and can lead to infinite loops.',
        suggestions: null,
      }).withDetails({
        kind: 'error',
        loc: instr.loc ?? callee.loc,
        message: 'Found setState() in render',
      })
    );
  }
}
```

Apply this standard anywhere you see an `invariant` risk, a missing registry/shape/metadata problem, or a diagnostic that could be more precise or more fixable.