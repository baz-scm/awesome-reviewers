---
title: Prefer explicit dataflow
description: 'Code should make its intent and governing logic unambiguous.


  - **Avoid hybrid reasoning:** If the validity of a branch is already determined
  by **dataflow**, don’t add extra **type-guard checks** just to “help” the reader.
  Remove guards like `isXType(...)` when they don’t materially change the control
  flow.'
repository: facebook/react#b10
label: Code Style
language: TypeScript
comments_count: 2
repository_stars: 251894
---

Code should make its intent and governing logic unambiguous.

- **Avoid hybrid reasoning:** If the validity of a branch is already determined by **dataflow**, don’t add extra **type-guard checks** just to “help” the reader. Remove guards like `isXType(...)` when they don’t materially change the control flow.
- **Make side effects explicit:** Helpers that *write into* parameters should either (a) **return** the computed data and let the caller merge, or (b) make mutation obvious in the signature/name.

Example (dataflow-only guard):
```ts
for (const operand of eachInstructionOperand(instr)) {
  // If dataflow guarantees what `operand.identifier` represents,
  // avoid redundant typing checks here.
  if (isSetStateType(operand.identifier)) {
    // ...
  }
}
```
Prefer removing the redundant `isSetStateType` check when unnecessary.

Example (explicit mutation vs return):
```ts
type IdentifierSet = Set<IdentifierId>;

function collectDeps(fn: FunctionExpression | undefined): IdentifierSet {
  const deps: IdentifierSet = new Set();
  if (!fn) return deps;
  // fill deps
  return deps;
}

// caller merges
for (const id of collectDeps(fn)) {
  deps.add(id);
}
```
If you do use an out-parameter, ensure the API clearly signals it (e.g., parameter name like `outDeps` and/or comments), so readers immediately understand the mutation.