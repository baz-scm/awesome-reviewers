---
title: Semantic Naming Consistency
description: 'Names you generate or transform should be semantic, consistent, and
  minimal. Concretely:


  - Avoid redundant renames in code transformations. Prefer shorthand destructuring
  and correct key forms for non-identifier property names.'
repository: facebook/react#b6
label: Naming Conventions
language: Markdown
comments_count: 4
repository_stars: 251888
---

Names you generate or transform should be semantic, consistent, and minimal. Concretely:

- Avoid redundant renames in code transformations. Prefer shorthand destructuring and correct key forms for non-identifier property names.
  ```js
  // Prefer
  const { disabled, 'aria-label': ariaLabel } = props;
  // Not
  // const { disabled: disabled, ariaLabel: ariaLabel } = props;
  ```

- Keep terminology consistent across the API surface. If two concepts differ by data shape (e.g., trace vs structured list), encode that difference explicitly with clear, consistent suffixes rather than overloading a single term.
  - Example: use `..._stack_trace` for V8-like frames and `..._stack` for the structured owner list.

- Preserve meaningful origin names and don’t add noise to derived identifiers. Only rename when the original entity is truly anonymous/needs normalization; when a known framework pattern guarantees a single item (e.g., a builtin React hook argument), omit meaningless indices like `arg0`.
  - Example direction: prefer `useEffect` over `useEffect(arg0)` for built-in effect hooks.