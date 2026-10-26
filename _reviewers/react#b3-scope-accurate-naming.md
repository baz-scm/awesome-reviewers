---
title: Scope-Accurate Naming
description: When naming logic (generated identifiers, rewritten globals, or boolean
  helpers) is involved, ensure the naming rules match the real scope/binding semantics
  and that names/comments reflect the exact meaning.
repository: facebook/react#b3
label: Naming Conventions
language: TypeScript
comments_count: 4
repository_stars: 251883
---

When naming logic (generated identifiers, rewritten globals, or boolean helpers) is involved, ensure the naming rules match the real scope/binding semantics and that names/comments reflect the exact meaning.

Apply these practices:
- Scope-bounded generation: If you sanitize or generate identifiers (e.g., JSX prop keys), deduplicate only within the boundary where collisions can occur (often the outlined function’s fresh scope). Avoid alternative UID strategies that over-fire into outer-scope naming and produce unnecessary output diffs.
- Binding-aware rewrites: When rewriting known globals (e.g., `Symbol`), only rewrite when the reference’s binding is truly the global one—do not rewrite shadowed identifiers.
- Comment precision: If parser validation guarantees certain identifier shapes, describe rules as “valid identifiers that reach this path” rather than implying all strings are handled.
- Semantic helper naming: For boolean helpers that aggregate across multiple items, ensure the name matches the semantics (e.g., `hasError()`/`isError()` should clearly mean “any detail has severity X”).

Example (binding-aware rewrite gate):
```ts
case 'LoadGlobal': {
  if (instrValue.binding.kind === 'Global' && instrValue.binding.name === 'Symbol') {
    value = codegenGlobalAccess(cx, 'Symbol');
    break;
  }
  // otherwise, leave shadowed/local Symbol untouched
}
```