---
title: Scope-Aware Identifier Naming
description: 'When transforming, generating, or rewriting identifiers, make the naming
  rule explicit and scope-aware.


  Apply these standards:

  1) **Validate before classifying**: Only assume an input is a valid identifier if
  the parser/compiler guarantees it; otherwise validate explicitly and/or keep comments
  precise (“all other **valid** identifiers …”).'
repository: facebook/react#b10
label: Naming Conventions
language: TypeScript
comments_count: 6
repository_stars: 251894
---

When transforming, generating, or rewriting identifiers, make the naming rule explicit and scope-aware.

Apply these standards:
1) **Validate before classifying**: Only assume an input is a valid identifier if the parser/compiler guarantees it; otherwise validate explicitly and/or keep comments precise (“all other **valid** identifiers …”).
2) **Use scope-safe uniqueness**: Prefer compiler/scope APIs for fresh IDs (e.g., `programContext.newUuid()` / `newUid` equivalents) when uniqueness must hold across scopes. Don’t treat a local dedup set (`seen`) as a substitute for scope-safe uniqueness.
3) **Respect shadowing**: When rewriting references (e.g., globals like `Symbol`), use binding metadata (such as `binding.kind === 'Global'`) so shadowed bindings are not incorrectly rewritten to globals.
4) **Model special cases explicitly**: If an identifier/key is structurally different (e.g., numeric object keys), consider representing it as a distinct variant instead of relying on lossy ad-hoc conversion.
5) **Cover semantic ambiguities with tests**: For rules that infer meaning from names/patterns (e.g., “PascalCase implies component”), add tests for both valid and ambiguous/false-positive wrapper patterns.

Example pattern for globals:
```ts
// Only rewrite true globals; never rewrite shadowed bindings.
if (binding.kind === 'Global' && binding.name === 'Symbol') {
  value = codegenGlobalAccess(cx, 'Symbol');
}
```