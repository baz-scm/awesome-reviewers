---
title: Actionable compiler errors
description: Ensure error handling in the compiler is both *preventive* (avoid hitting
  invariant-only failures) and *diagnostic* (when something is impossible or invalid,
  fail with precise, compiler-reported information).
repository: facebook/react#b5
label: Error Handling
language: TypeScript
comments_count: 4
repository_stars: 251886
---

Ensure error handling in the compiler is both *preventive* (avoid hitting invariant-only failures) and *diagnostic* (when something is impossible or invalid, fail with precise, compiler-reported information).

Apply these rules:
1) **Make definitions complete and consistent**: if an IR/HIR uses an ID (e.g., a shape id), guarantee that a corresponding definition exists. Don’t rely on downstream property resolution to crash via an unreported invariant.
2) **Encode impossible states with explicit invariants that carry `loc`**: for control-flow assumptions (e.g., “no nested memo calls”), use an invariant with the relevant source location so failures are actionable rather than silently ignored.
3) **Propagate source locations through all diagnostic-relevant IR variants**: when you add/rename IR kinds (e.g., an “Aggregate” dependency kind), include `loc` so the compiler can later construct precise error messages and automated fix suggestions.
4) **When removing defensive checks, replace them with enforced assumptions**: if logic assumes inputs are already validated (e.g., only known ids), either keep the assertion/invariant (ideally compiler-reported) or add a clear precondition proof point; otherwise failures can regress into non-surfaced crashes.

Example pattern:
```ts
function onStartMemoize(value: StartMemoize, ...): void {
  CompilerError.simpleInvariant(startMemo == null, {
    reason: 'Unexpected nested memo calls',
    loc: value.loc,
  });
  // ...
}

// When adding a new IR kind used for diagnostics:
type Aggregate = { kind: 'Aggregate'; dependencies: Set<InferredDependency>; loc: SourceLocation };
```

This approach reduces “silent” invariant failures and improves the quality of diagnostics and auto-fixes for developers using the compiler.