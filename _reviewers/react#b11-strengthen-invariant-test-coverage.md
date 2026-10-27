---
title: Strengthen invariant test coverage
description: When validating compiler/codegen correctness (especially range/loc preservation),
  don’t rely on narrow or declaration-scoped checks. Add tests that enforce the stated
  invariant across the entire relevant output structure, ensure parity across backends,
  and include fixtures for edge shapes that lack source location metadata.
repository: facebook/react#b11
label: Testing
language: TypeScript
comments_count: 2
repository_stars: 251894
---

When validating compiler/codegen correctness (especially range/loc preservation), don’t rely on narrow or declaration-scoped checks. Add tests that enforce the stated invariant across the entire relevant output structure, ensure parity across backends, and include fixtures for edge shapes that lack source location metadata.

How to apply:
- Prefer global invariant assertions: for every output node that has numeric `start`/`end` and `loc.index`, assert the mapping consistency (and basic ordering).
- Ensure both backends run the same invariant checks.
- Add/extend fixtures for known lossy cases (e.g., nodes whose hoisted declarators have no `loc`, for-in/for-of declarators without `loc`, etc.).
- If some cases can’t be made to pass immediately, treat them as explicit follow-ups: add fixtures or document the exact missing node kinds.

Example invariant (adapted):
```ts
for (const node of outputAstNodes) {
  if (typeof node.start === 'number' && typeof node.end === 'number' && node.loc?.index != null) {
    assert(node.start === node.loc.start.index);
    assert(node.end === node.loc.end.index);
    assert(node.start <= node.end);
  }
}
```

Acceptance bar: the invariant holds across the whole output AST for both backends, with regression tests for shifted/missing/partial offset scenarios and explicit coverage for the edge node categories you’ve identified as currently lossy.