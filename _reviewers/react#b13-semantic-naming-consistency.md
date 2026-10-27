---
title: Semantic naming consistency
description: 'When transforming or generating names, keep identifiers semantic, stable,
  and idiomatic:


  - Use idiomatic destructuring bindings for known prop/attribute names:'
repository: facebook/react#b13
label: Naming Conventions
language: Markdown
comments_count: 3
repository_stars: 251893
---

When transforming or generating names, keep identifiers semantic, stable, and idiomatic:

- Use idiomatic destructuring bindings for known prop/attribute names:
  - Prefer shorthand when the binding name matches the property name.
  - Use quoted keys for attribute names that aren’t valid identifier names (e.g., hyphenated keys).

  ```js
  // Prefer
  const { disabled, 'aria-label': ariaLabel } = t0;

  // Avoid
  const { disabled: disabled, ariaLabel: ariaLabel } = t0;
  ```

- Preserve developer-provided names: don’t rename functions that already have meaningful names. Only synthesize names/wrappers for functions that were truly anonymous (e.g., function expressions assigned to variables).

- Keep generated names minimal and semantics-based for well-known constructs (especially built-in hooks). Avoid over-specific identifiers like `useEffect(arg0)` when a stable, simpler name like `useEffect` (or equivalent) better reflects semantics.

Applying these rules will reduce noisy, fragile identifier differences and improve readability/traceability across code transformations.