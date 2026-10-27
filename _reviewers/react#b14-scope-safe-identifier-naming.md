---
title: Scope-Safe Identifier Naming
description: 'When generating or rewriting identifiers/names, treat naming as a correctness
  problem—not just formatting.


  - **Sanitize without losing semantics:** If an original property/name is not a valid
  JS identifier (e.g. `aria-label`), transform it into a safe identifier for destructuring/usage,
  but preserve the original meaning at the call site.'
repository: facebook/react#b14
label: Naming Conventions
language: TypeScript
comments_count: 3
repository_stars: 251893
---

When generating or rewriting identifiers/names, treat naming as a correctness problem—not just formatting.

- **Sanitize without losing semantics:** If an original property/name is not a valid JS identifier (e.g. `aria-label`), transform it into a safe identifier for destructuring/usage, but preserve the original meaning at the call site.
- **Ensure uniqueness using scope-aware, compiler-provided mechanisms:** Avoid “best-effort” deduping that can miss in-scope conflicts. Use the compiler’s UID/name generation API (e.g. `programContext.newUuid()` / `newUid`) when uniqueness must be guaranteed across the compiler’s identifier graph.
- **Only rewrite when binding semantics are unambiguous:** If rewriting special/global identifiers (e.g. `Symbol`), guard by binding information (e.g. rewrite only when `binding.kind === 'Global'`), so shadowed locals are never changed.
- **For naming-based heuristics, add targeted tests:** If logic depends on naming/casing patterns (e.g. “PascalCase implies component”), include both valid and counterexample wrappers in tests.

Example (scope-aware global handling):
```ts
case 'LoadGlobal': {
  if (instrValue.binding.kind === 'Global' && instrValue.binding.name === 'Symbol') {
    value = codegenGlobalAccess(cx, 'Symbol');
    break;
  }
}
```