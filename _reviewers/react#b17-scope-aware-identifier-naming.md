---
title: Scope-Aware Identifier Naming
description: 'When introducing or transforming identifiers (variable names, generated
  prop bindings, temp names), follow these rules:


  1) Use the correct scope-aware uniqueness API'
repository: facebook/react#b17
label: Naming Conventions
language: TypeScript
comments_count: 2
repository_stars: 251891
---

When introducing or transforming identifiers (variable names, generated prop bindings, temp names), follow these rules:

1) Use the correct scope-aware uniqueness API
- Prefer the program/scope facility for unique names (e.g., `programContext.newUuid()`/equivalent) instead of relying on ad-hoc “seen”/partial sets that may miss in-scope identifiers.

2) Deduplicate only within the real collision boundary
- If the generated names live in a fresh, isolated scope, dedupe based on that scope’s collision domain (e.g., per-JSX-element prop mapping after sanitization), not on outer-scope identifiers.

3) Sanitize deterministically into valid identifiers
- If an input name isn’t a valid JS identifier (e.g., JSX attributes like `aria-label`), convert it in a deterministic way while preserving the mapping semantics at the call site/destructuring (e.g., keep the original key where required, and bind a valid identifier in code).

4) Keep naming-adjacent metadata precise
- If you name/annotate parameters/effects alongside an identifier (e.g., `with(index, value)`), ensure the associated semantics match the actual signature.

Example pattern (sanitizing JSX prop names while avoiding collisions within the right scope):
```ts
function isHyphenatedJsxProp(originalName: string): boolean {
  return !isValidIdentifier(originalName) && /^[a-zA-Z_][\w.-]*$/.test(originalName);
}

// In the outlined function’s own fresh scope:
// - dedupe per JSX element prop mapping after sanitization
// - generate unique identifiers using the scope/program API
// - preserve original prop keys where needed (quoted destructuring)
```