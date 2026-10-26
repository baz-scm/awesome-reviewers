---
title: Prefer user-facing diagnostics
description: When validating or transforming inputs, avoid “silent” failures caused
  by internal invariants or missing definitions. If an error can be triggered by user
  code (directly or indirectly), surface it as a structured compiler diagnostic with
  enough context to recover (at minimum `loc`, ideally a `suggestions`/automated fix).
repository: facebook/react#b1
label: Error Handling
language: TypeScript
comments_count: 5
repository_stars: 251878
---

When validating or transforming inputs, avoid “silent” failures caused by internal invariants or missing definitions. If an error can be triggered by user code (directly or indirectly), surface it as a structured compiler diagnostic with enough context to recover (at minimum `loc`, ideally a `suggestions`/automated fix).

Additionally, treat internal invariants as a contract: either (a) prove the invariant can’t be violated (then assertions are safe), or (b) don’t let an unreported invariant throw—convert it into a `CompilerError.invariant(...)` that’s meaningful, or into a user-facing diagnostic.

Example pattern:
```ts
if (/* user-triggerable condition */) {
  errors.pushDiagnostic(
    CompilerDiagnostic.create({
      category: ErrorCategory.SomeValidation,
      reason: '...',
      description: '...',
      suggestions: /* actionable fix when possible */ null,
    }).withDetails({
      kind: 'error',
      loc: failingNode.loc,
      message: 'Found ...'
    }),
  );
} else {
  CompilerError.invariant(/* proven internal condition */, { reason: 'Compiler internal error: ...' });
}
```
This reduces opaque compiler crashes, prevents eslint/infra gaps from turning errors into silent failures, and improves developer/user experience via precise locations and (when feasible) automated suggestions.