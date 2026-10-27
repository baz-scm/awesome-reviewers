---
title: Explicit null/undefined checks
description: Use explicit `!= null` checks (which cover both `null` and `undefined`)
  rather than relying on truthiness or chaining multiple optional accesses together,
  and prefer narrowing a value once via an explicit check instead of re-deriving or
  casting it later with `as`. Be especially careful when combining optional chaining
  (`?.`) with nullish coalescing (`??`):...
repository: facebook/react#b19
label: Null Handling
language: TypeScript
comments_count: 4
repository_stars: 251893
---

Use explicit `!= null` checks (which cover both `null` and `undefined`) rather than relying on truthiness or chaining multiple optional accesses together, and prefer narrowing a value once via an explicit check instead of re-deriving or casting it later with `as`. Be especially careful when combining optional chaining (`?.`) with nullish coalescing (`??`): TypeScript may not infer the left-hand side as nullable in all cases, causing the right-hand side fallback to silently never execute. Write out the nullability conditions explicitly (e.g. `a?.b ?? fallback` should be validated against `a == null ? fallback : a.b`) so the intended behavior is unambiguous and verified by tests, especially for edge cases like one operand being null while another is present (e.g. recomputing a location range when only one of two optional values is set).

Example:
```ts
// Prefer explicit, simple null check over truthiness/casts
return t.assignmentExpression(
  '=',
  declarator.id as t.LVal,
  declarator.init != null ? declarator.init : t.identifier('undefined'),
);

// After narrowing, reuse the narrowed value instead of re-casting
if (lvalue != null) {
  temporaries.set(lvalId, {
    root: {kind: 'NamedLocal', value: {...lvalue}},
    path: [],
  });
}

// Avoid subtle bugs from combining ?. and ?? — verify fallback actually triggers
const id = block.instructions[0]?.id ?? block.terminal.id; // double-check LHS nullability
```