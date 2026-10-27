---
title: Scope-Aware Identifier Naming
description: When changing or generating identifiers (including JSX prop destructuring
  names or rewriting built-in/global references), make the transformation *binding-
  and scope-aware* so you avoid unintended renames and shadowing bugs.
repository: facebook/react#b8
label: Naming Conventions
language: TypeScript
comments_count: 2
repository_stars: 251889
---

When changing or generating identifiers (including JSX prop destructuring names or rewriting built-in/global references), make the transformation *binding- and scope-aware* so you avoid unintended renames and shadowing bugs.

Apply these rules:
- **Sanitize deterministically, then dedupe at the right boundary.** If multiple inputs normalize to the same identifier (e.g., `aria-*` → same camelCase form), dedupe only where the collision can happen (e.g., within the outlined function/within one JSX element), rather than renaming everything via a broader uid strategy.
- **Don’t over-fire global/uid generation.** If a broader “always-unique” uid helper forces renaming that isn’t necessary for correctness, it can break snapshots/eval output even when semantics appear safe.
- **When rewriting special identifiers, check binding kind.** Only rewrite a reference to a global built-in if the reference is actually bound to the global; otherwise preserve shadowed locals.

Example (binding-gated global rewrite):
```ts
case 'LoadGlobal': {
  if (instrValue.binding.kind === 'Global' && instrValue.binding.name === 'Symbol') {
    value = codegenGlobalAccess(cx, 'Symbol');
  }
  break;
}
```

Example (local-safe prop naming):
- Keep original/compatible prop names when possible, sanitize only when needed, and use a *local* collision guard (e.g., a `seen` set) to prevent duplicate destructuring keys after normalization.