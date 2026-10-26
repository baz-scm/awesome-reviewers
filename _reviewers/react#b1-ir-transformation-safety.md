---
title: IR Transformation Safety
description: 'When implementing compiler/IR rewrites or analyses, treat correctness
  as an algorithmic contract: guard every transformation with precise semantic and
  structural preconditions, and use fixpoint-style iteration/caching when derivations
  can depend on other derivations.'
repository: facebook/react#b1
label: Algorithms
language: TypeScript
comments_count: 6
repository_stars: 251878
---

When implementing compiler/IR rewrites or analyses, treat correctness as an algorithmic contract: guard every transformation with precise semantic and structural preconditions, and use fixpoint-style iteration/caching when derivations can depend on other derivations.

Apply these rules:

1) Gate rewrites using binding/scope metadata (never rely on name-only heuristics)
- If rewriting identifier references, ensure you discriminate shadowed vs global/module bindings via the IR’s binding/kind information.
- Example pattern:
  ```ts
  if (binding.kind === 'Global' && binding.name === 'Symbol') {
    // safe: only the true global
  }
  ```

2) Validate IR structural invariants before rewriting control flow / value constructs
- If you replace a terminal (e.g., ternary -> goto) or rewrite value expressions (e.g., SequenceExpression), confirm the target block/value-block shape matches what your transformation assumes.
- Add checks for nested value blocks / expected fallthrough structure rather than assuming a shallow graph.

3) Make scope assumptions explicit and assert them
- If you convert a construct that previously disallowed declarations in a value block (e.g., `const t0 = expr` inside a SequenceExpression), only do so when the declarator targets are guaranteed in-scope (typically compiler-generated temporaries).
- Prefer a runtime invariant or an explicit check/fixture for the “in-scope temporaries” assumption.

4) Use fixed-point iteration for dataflow/derivation analyses
- When derivations may be discovered through Phi nodes, nested functions, or cascading effects, implement an iterative process with a snapshot/hasChanges loop over a derivation cache rather than a single pass.

5) For outlining/transform eligibility, compare against the function’s context
- Checks like “find outer-scope reads” must be interpreted relative to what the function expression’s context already accounts for (e.g., LoadContext/StoreContext semantics). Otherwise you may incorrectly disqualify or incorrectly allow outlining.

6) Add targeted regression fixtures for each edge case
- Every time you introduce a guard for a specific failure mode (scope shadowing, nested value blocks, StoreContext, etc.), add a fixture that covers that exact shape so the invariant stays enforced over time.