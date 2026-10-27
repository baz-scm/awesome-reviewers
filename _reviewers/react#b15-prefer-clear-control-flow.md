---
title: Prefer clear control flow
description: "Default to readable, consistent code that makes intent obvious.\n\n\
  - Keep control flow linear: avoid unnecessary `else` after an early `return`.\n\
  \  ```js"
repository: facebook/react#b15
label: Code Style
language: JavaScript
comments_count: 6
repository_stars: 251891
---

Default to readable, consistent code that makes intent obvious.

- Keep control flow linear: avoid unnecessary `else` after an early `return`.
  ```js
  if (cond) {
    return doScript();
  }
  return doData();
  ```
- Don’t add “obvious behavior” comments (e.g., comments that restate what the code already shows); put effort into fixing the real issue instead.
- Use strict equality by default (`===`/`!==`) unless there is a documented reason for loose equality.
- Prefer proper typing/annotations over suppressions like `$FlowFixMe[missing-local-annot]`; annotate callback params locally so the type system can validate the code.
- Avoid hard-to-read formatting patterns like multi-line ternaries; use `if`/early returns for clarity.

This improves consistency, reduces reviewer overhead, and prevents hidden style debt from accumulating.