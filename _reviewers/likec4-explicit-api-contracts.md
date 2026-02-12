---
title: Explicit API contracts
description: 'Require API types and public interfaces to express clear, enforceable
  contracts: guarantee invariants, normalize variant shapes, and make compatibility
  choices explicit.'
repository: likec4/likec4
label: API
language: TypeScript
comments_count: 5
repository_stars: 2582
---

Require API types and public interfaces to express clear, enforceable contracts: guarantee invariants, normalize variant shapes, and make compatibility choices explicit.

Why: Clear types prevent subtle bugs, make callers’ expectations explicit, and make evolving an API safer (clients can rely on invariants or intentionally opt into legacy shapes).

How to apply (practical rules):
- Prefer precise return types that guarantee required fields instead of vague or permissive types. If a function promises to return a node with a specific model FQN, express that in the signature.
  Example:
  function findNodeByModelFqn<T extends NodeWithData>(
    nodes: Types.Node[],
    modelFqn: Fqn
  ): (Types.Node & { data: { modelFqn: Fqn } }) | null

- When two fields are conceptually paired, represent them as a single array of paired objects so their relationship and lengths are guaranteed:
  // instead of separate includePaths?: URI[] and includePathsAsStrings?: ProjectFolder[]
  includePaths?: Array<{ uri: URI, folder: ProjectFolder }>

- Normalize variant/union shapes using discriminants and common base types; provide parsing/mapping helpers that convert legacy or multiple AST/kinds into a single canonical representation. When you must keep legacy shapes, add an explicit flag or an optional legacy field rather than implicit differences:
  type DynamicBranchCollectionBase = { branchId: string; astPath: string; kind: 'parallel' | 'alternate'; paths: DynamicBranchPath[] }
  interface DynamicParallelBranch extends DynamicBranchCollectionBase { kind: 'parallel'; isLegacyParallel?: boolean }

  Use small helpers to map input kinds to the normalized model:
  function getBranchKind(astKind: string): 'parallel' | 'alternate' {
    return astKind === 'alternate' || astKind === 'alt' ? 'alternate' : 'parallel'
  }

- Be explicit about semantic decisions that affect consumers (e.g., whether nested parallels are allowed or should be flattened). Either enforce the rule in the parser/validator or document/parameterize the behavior so callers/layout code can handle it deterministically.

Checklist for PR authors:
- Does each public function/type guarantee the required fields (no implicit assumptions)? If not, tighten the types.
- Are related arrays or fields paired as a single structure when their association matters? If not, refactor to a paired array/object.
- Are variant shapes represented by a canonical discriminated union? Is legacy behaviour explicit (flagged) and handled in parsing code?
- Have you documented any semantic choices that affect client behaviour (nesting rules, flattening policies)?

Applying these rules will make API boundaries explicit, reduce accidental breakage, and make evolution more controlled and predictable.