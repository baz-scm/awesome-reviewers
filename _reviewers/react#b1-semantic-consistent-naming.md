---
title: Semantic Consistent Naming
description: 'Use naming that is semantically consistent, stable, and minimal—avoiding
  redundant renames and noisy/generated ambiguity.


  Practical rules:

  1) Avoid redundant renames in destructuring'
repository: facebook/react#b1
label: Naming Conventions
language: Markdown
comments_count: 4
repository_stars: 251878
---

Use naming that is semantically consistent, stable, and minimal—avoiding redundant renames and noisy/generated ambiguity.

Practical rules:
1) Avoid redundant renames in destructuring
- Prefer identifier shorthand when the target name matches.
- For non-identifier keys (e.g. containing hyphens), use quoted property keys.

```js
// Prefer:
const { disabled, 'aria-label': ariaLabel } = propsOrT0;

// Avoid redundant renames like:
// const { disabled: disabled, ariaLabel: ariaLabel } = ...
```

2) Keep terminology consistent in public APIs/tools
- If you use a term family (e.g. “owner stack”), don’t switch to a different term for similar concepts.
- When return types differ, differentiate with a suffix that states what the return is (not a different base term).

3) Ensure generated/transformed names are stable and not noisy
- Only rename/wrap when the source is actually anonymous/unstable (don’t change behavior just because something is “nested”).
- In generated name strings, avoid arg-index clutter when a special-case/built-in pattern can produce a cleaner stable name; if you must include an argument index, do so only when it meaningfully disambiguates (e.g. multiple anonymous function arguments).

Applying this standard will improve readability, reduce confusion for API consumers, and keep transformed/generated identifiers easier to compare and debug.