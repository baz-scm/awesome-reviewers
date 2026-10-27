---
title: Prefer actionable diagnostics
description: 'When a compiler/validator relies on an assumption (e.g., a required
  HIR shape exists, a generated expression has an expected AST shape, a cache contains
  named places), avoid letting users hit raw `invariant` failures that may surface
  as hard crashes or silent compiler breakage. Instead:'
repository: facebook/react#b14
label: Error Handling
language: TypeScript
comments_count: 5
repository_stars: 251893
---

When a compiler/validator relies on an assumption (e.g., a required HIR shape exists, a generated expression has an expected AST shape, a cache contains named places), avoid letting users hit raw `invariant` failures that may surface as hard crashes or silent compiler breakage. Instead:

1) Ensure “external/known ids” are fully defined
- If you register a shape/id (e.g., a built-in shape id), also add/verify the concrete definition it resolves to, so property/type resolution doesn’t crash later.

2) Convert invariant-violations into structured compiler diagnostics
- If an invariant can be triggered by user code or by a missing/mismatched definition, emit a `CompilerDiagnostic` with at least:
  - a clear `reason`
  - `loc` (source location)
  - (when feasible) a `suggestions`/fix payload
- If the failure truly must be internal, either:
  - prove it’s unreachable (and optionally assert with a tighter invariant), or
  - add a precondition check earlier that produces a diagnostic rather than crashing.

3) Preserve correctness when relaxing structural checks
- If you change codegen/validation to allow additional shapes/paths, add targeted runtime/type tests for the previously-guaranteed cases (especially receiver/side-effect/typing-sensitive patterns) so you don’t trade an invariant crash for a later compilation failure.

Example pattern:
```ts
// Before: raw invariant that may surface as an unhelpful crash
CompilerError.invariant(condition, { reason: 'internal', loc: memberExpr.loc ?? null, ... });

// After: if it can be user-triggered, prefer diagnostic
if (!condition) {
  errors.pushDiagnostic(
    CompilerDiagnostic.create({
      category: ErrorCategory.Whatever,
      reason: 'Expected ... but saw ...',
      description: 'How to fix / what pattern is unsupported.',
      suggestions: /* optional */ null,
    }).withDetails({
      kind: 'error',
      loc: memberExpr.loc,
      message: 'Unsupported method call form',
    }),
  );
}
```
Apply this consistently to prevent hard-to-debug invariant failures and to make error reporting precise and actionable (including `loc` so fixes can be automated).