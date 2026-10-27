---
title: Safe nullish coalescing
description: When handling nullable or optional values, prefer concise, idiomatic
  null-check patterns (e.g. ternary or nullish coalescing) instead of verbose if/else
  branches, but always verify that the types involved genuinely reflect nullability—mixing
  optional chaining (`?.`) with nullish coalescing (`??`) can silently produce incorrect
  results if the left-hand...
repository: facebook/react#b20
label: Null Handling
language: TypeScript
comments_count: 3
repository_stars: 251895
---

When handling nullable or optional values, prefer concise, idiomatic null-check patterns (e.g. ternary or nullish coalescing) instead of verbose if/else branches, but always verify that the types involved genuinely reflect nullability—mixing optional chaining (`?.`) with nullish coalescing (`??`) can silently produce incorrect results if the left-hand expression's inferred type doesn't include `undefined`, since TypeScript will then ignore the `??` fallback and no error is raised.

For example, prefer:
```ts
const expr = declarator.init != null
  ? declarator.init
  : t.identifier('undefined');
```
over a longer if/else block.

But be cautious with code like:
```ts
block.instructions[0]?.id ?? block.terminal
```
If `block.instructions[0]?.id` is typed as always non-nullable (e.g. due to an incorrect array/index type), the `??` branch is dead code and the bug (using `block.terminal` instead of `block.terminal.id`) goes undetected. Always check the inferred type of the left-hand side of `??` to confirm it can actually be `null`/`undefined`, and when deriving optional data (such as source locations) that depend on another optional field, fall back on the smallest necessary piece of data (e.g. use `id.loc` directly when `init` is null, rather than constructing a compound value that assumes `init` exists).