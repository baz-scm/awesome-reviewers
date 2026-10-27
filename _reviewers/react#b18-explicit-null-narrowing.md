---
title: Explicit null narrowing
description: Prefer explicit null/undefined narrowing over type assertions or implicit
  assumptions about nullability. When a variable may be null or undefined, narrow
  it with a guard (e.g. `if (lvalue != null) { ... use lvalue ... }`) and reuse the
  narrowed binding instead of casting with `as Type`, which bypasses the type checker
  and can hide real bugs.
repository: facebook/react#b18
label: Null Handling
language: TypeScript
comments_count: 3
repository_stars: 251889
---

Prefer explicit null/undefined narrowing over type assertions or implicit assumptions about nullability. When a variable may be null or undefined, narrow it with a guard (e.g. `if (lvalue != null) { ... use lvalue ... }`) and reuse the narrowed binding instead of casting with `as Type`, which bypasses the type checker and can hide real bugs.

Be especially careful with array/collection index access combined with optional chaining and nullish coalescing, e.g. `block.instructions[0]?.id ?? block.terminal`. If the element type isn't statically marked optional, TypeScript won't flag the access as nullable, so the `?.` becomes a no-op and the intended `??` fallback never runs even though the element can be `undefined` at runtime (e.g. an empty array). In these cases, add an explicit length/undefined check instead of relying on `?.`/`??` to "just work":
```ts
const firstInstruction = block.instructions[0];
const id = firstInstruction !== undefined ? firstInstruction.id : block.terminal.id;
```

When simplifying or removing a null/undefined check because analysis shows the value is always defined by construction, don't just delete the check silently — replace it with a `CompilerError.invariant` (or equivalent assertion) so that any future violation of that assumption fails loudly instead of causing a silent null-reference bug.