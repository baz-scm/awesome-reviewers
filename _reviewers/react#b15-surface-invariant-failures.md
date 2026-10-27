---
title: Surface Invariant Failures
description: When your code relies on internal assumptions (registries, invariants,
  inferred metadata), ensure failures are (a) detected early, (b) reported clearly,
  and (c) tied back to source locations so you can produce precise fixes.
repository: facebook/react#b15
label: Error Handling
language: TypeScript
comments_count: 3
repository_stars: 251891
---

When your code relies on internal assumptions (registries, invariants, inferred metadata), ensure failures are (a) detected early, (b) reported clearly, and (c) tied back to source locations so you can produce precise fixes.

Apply this standard:
1) Validate completeness of registries/ids
- If you register a shape/type/id (e.g., adding a shape id to a built-in map), ensure the corresponding definition exists immediately (startup/build-time). Missing definitions should fail fast with a clear compiler error message rather than a downstream invariant.

2) Make invariant failures user-visible and actionable
- For internal assumptions, keep explicit checks, but ensure the resulting error is a surfaced compiler diagnostic (with a helpful reason/message), not a raw invariant that might be missed by lint tooling.

Example pattern:
```ts
// Early, fail-fast check during initialization
if (!shapeDefinitions.has(ReanimatedSharedValueId)) {
  throw new Error(
    `Compiler initialization error: missing shape definition for ${ReanimatedSharedValueId}`
  );
}

// Later, guard an invariant with a surfaced compiler error
CompilerError.invariant(isNamedIdentifier(sourceMetadata.place), {
  reason:
    'Compiler internal error: expected derivation entries to always reference named variables',
});
```

3) Preserve SourceLocation for precise diagnostics and suggestions
- When building validation/analysis nodes, carry `loc: SourceLocation` (or equivalent) so errors can highlight the exact code region and automated suggestions can target the correct manual deps array.

Outcome: inconsistent internal state won’t slip through as “silent” failures; when it does fail, the user sees a clear diagnostic anchored to their source, and the compiler can offer targeted remediation (suggestions).