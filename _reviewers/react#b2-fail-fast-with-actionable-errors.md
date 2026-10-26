---
title: Fail Fast With Actionable Errors
description: 'Enforce correctness assumptions early and make failures actionable.


  - Ensure referenced IDs/shapes/metadata are fully defined before use; missing definitions
  should fail fast rather than manifest later as an unreported invariant.'
repository: facebook/react#b2
label: Error Handling
language: TypeScript
comments_count: 3
repository_stars: 251882
---

Enforce correctness assumptions early and make failures actionable.

- Ensure referenced IDs/shapes/metadata are fully defined before use; missing definitions should fail fast rather than manifest later as an unreported invariant.
- When code assumes “this can’t happen” (e.g., because earlier validation guarantees it), enforce that assumption with an explicit invariant/assert instead of silently skipping/continuing.
- When producing diagnostics or automated suggestions, preserve source context (e.g., `loc: SourceLocation`) so errors can point to the right code and fixes can be constructed.

Example pattern:

```ts
// 1) Fail fast on missing definitions
addObject(BUILTIN_SHAPES, ReanimatedSharedValueId, []); // ensure shape exists

// 2) Enforce unreachable states explicitly
const sourceMetadata = this.cache.get(id);
if (sourceMetadata === undefined) {
  throw CompilerError.invariant('Expected known sourceId in derivation cache');
}

// 3) Preserve context for actionable suggestions
type Aggregate = { kind: 'Aggregate'; dependencies: Set<InferredDependency>; loc: SourceLocation };
```

Apply this to validation/analysis code paths so errors are both reliable (no silent compiler failures) and useful (pointing to the right location and enabling suggestions).