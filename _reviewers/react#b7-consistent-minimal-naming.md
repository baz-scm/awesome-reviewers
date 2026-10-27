---
title: Consistent Minimal Naming
description: 'Use naming conventions that are semantically precise, stable, and minimal—avoid
  renaming/extra disambiguation when it doesn’t add meaning.


  Apply these rules:'
repository: facebook/react#b7
label: Naming Conventions
language: Markdown
comments_count: 4
repository_stars: 251888
---

Use naming conventions that are semantically precise, stable, and minimal—avoid renaming/extra disambiguation when it doesn’t add meaning.

Apply these rules:
1) **Avoid unnecessary aliasing**: if the identifier name already matches, prefer shorthand rather than `x: x`.
2) **Use correct destructuring key syntax**: for non-identifier property names (e.g. dashed names), destructure using a quoted key.
3) **Keep terminology consistent across related concepts**: don’t mix terms like “stack” vs “branch” when users already associate “stack” with a specific concept; if the returned data shape differs, reflect that in a clear suffix.
4) **Make generated labels minimal**: remove redundant parts (like `arg0`) unless they’re required to disambiguate multiple anonymous/function arguments or multiple candidates.

Example (naming clarity in destructuring):
```js
// Prefer shorthand when possible
const { disabled } = obj;

// Use quoted keys for special property names
const { 'aria-label': ariaLabel } = obj;
```

Example (minimal generated labels):
- If there is only one anonymous function argument (or a builtin/special case), prefer `useEffect` over `useEffect(arg0)`.
- If multiple anonymous arguments exist, include indexes only then to disambiguate.