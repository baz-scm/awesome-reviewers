---
title: Scope-aware identifier derivation
description: 'When you derive or rename identifiers (e.g., from JSX attribute/tag
  names, object keys, or generated temporaries), follow these rules:


  1) Validate/normalize to a valid identifier form'
repository: facebook/react#b15
label: Naming Conventions
language: TypeScript
comments_count: 4
repository_stars: 251891
---

When you derive or rename identifiers (e.g., from JSX attribute/tag names, object keys, or generated temporaries), follow these rules:

1) Validate/normalize to a valid identifier form
- If the source can produce non-identifier keys/names (numeric literals, hyphenated props like `aria-label`), explicitly transform them into an identifier-safe representation.
- If your AST model can’t represent the transformed form cleanly, consider adding/using a dedicated variant rather than overloading existing ones.

2) Ensure uniqueness using the correct scope mechanism
- Don’t rely on “seen”/local deduplication alone if it may miss the real scope boundary.
- Prefer the project’s authoritative unique-id generator (e.g., `programContext.newUuid()` / equivalent) so names can’t collide across generated code paths.

3) Be scope/binding-aware for globals vs shadows
- Only rewrite/handle globals when the binding metadata proves it’s truly global.
- If a name (like `Symbol`) can be shadowed, gate any special handling on binding kind so shadowed references aren’t incorrectly rewritten.

4) Keep comments consistent with parser guarantees
- If code assumes certain identifier validity (because the parser already rejects invalid syntax), state that precisely (e.g., “only valid identifiers reach this branch”).

Example (scope-safe uniqueness + binding-kind guarding):
```ts
// Uniqueness: don’t depend solely on a partial `seen` set.
const name = env.programContext.newUuid(baseName);
// Binding-kind safety: only treat as global when proven.
if (binding.kind === 'Global' && binding.name === 'Symbol') {
  value = codegenGlobalAccess(cx, 'Symbol');
}
```

This keeps generated names predictable, prevents collisions, and avoids incorrect rewrites—all core aspects of naming conventions in code generators and transforms.