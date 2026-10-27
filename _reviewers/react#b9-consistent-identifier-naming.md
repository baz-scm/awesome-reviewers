---
title: Consistent Identifier Naming
description: 'Maintain identifier clarity and consistency:


  - Destructuring: use shorthand when the property key and local variable name match;
  when the property key isn’t a valid identifier (or must match an exact prop like
  `aria-label`), destructure with the correct quoted key.'
repository: facebook/react#b9
label: Naming Conventions
language: Markdown
comments_count: 3
repository_stars: 251891
---

Maintain identifier clarity and consistency:

- Destructuring: use shorthand when the property key and local variable name match; when the property key isn’t a valid identifier (or must match an exact prop like `aria-label`), destructure with the correct quoted key.
- Function naming: preserve existing function names; only rename/wrap anonymous/derived functions when needed for stable semantics, and base the introduced name on the assignment context.
- Avoid naming noise: don’t include redundant argument indices (e.g., `arg0`) when a builtin/special-case context makes it unambiguous.

Example (destructuring):
```js
// Prefer shorthand when possible
const { disabled } = t0;

// Quote keys that must match exact prop names
const { 'aria-label': ariaLabel } = t0;
```

Example (function naming policy):
- Keep a named function as-is.
- If an anonymous inner function is assigned via a variable (e.g., `named > inner`), give it a stable name derived from that assignment context.