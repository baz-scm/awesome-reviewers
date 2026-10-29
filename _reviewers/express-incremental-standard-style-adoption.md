---
title: Incremental standard-style adoption
description: The codebase is migrating toward the `standard` JavaScript style (no
  semicolons, multiple `const`/`let` declarations instead of comma-chained `var`,
  unindented chained method calls, space before function parentheses, etc.). Apply
  this style only to the lines you are already modifying, not as a wholesale reformat
  of untouched code — unrelated...
repository: expressjs/Express
label: Code Style
language: JavaScript
comments_count: 9
repository_stars: 69579
---

The codebase is migrating toward the `standard` JavaScript style (no semicolons, multiple `const`/`let` declarations instead of comma-chained `var`, unindented chained method calls, space before function parentheses, etc.). Apply this style only to the lines you are already modifying, not as a wholesale reformat of untouched code — unrelated whitespace/semicolon/indentation changes make diffs noisy and harder to review. For example, when editing a line in an existing file, bring just that line into `standard` style:

```js
// before (touched line)
res.send('Hello form root route.');
// after
res.send('Hello from root route.')
```

Before introducing newer syntax (ES6 classes, `let`/`const`, template literals, spread/rest, arrow functions, etc.), verify it is actually supported by the current ESLint configuration and the target Node/browser compatibility for that branch — some branches (e.g. the 4.x `main` branch) intentionally restrict ES6+ features for compatibility, and using unsupported syntax will fail `npm run lint` or break older runtimes. If you believe the lint rules should be updated to allow a feature, raise that as a separate, explicit change rather than mixing it into a feature PR. When in doubt, mimic the surrounding code's existing style/era rather than introducing a stylistic one-off.