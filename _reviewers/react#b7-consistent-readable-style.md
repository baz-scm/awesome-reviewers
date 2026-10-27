---
title: Consistent, readable style
description: 'Follow a consistent, low-noise coding style so reviews focus on logic,
  not formatting/annotations.


  - Use strict equality by default: `a === b` unless you have a documented reason
  for weak equality.'
repository: facebook/react#b7
label: Code Style
language: JavaScript
comments_count: 5
repository_stars: 251888
---

Follow a consistent, low-noise coding style so reviews focus on logic, not formatting/annotations.

- Use strict equality by default: `a === b` unless you have a documented reason for weak equality.
- Prefer shared helpers over ad-hoc checks when the project already has a canonical one (e.g., use `isArray(value)` instead of `Array.isArray(value)` when that’s the established pattern/Flow reason).
- Keep control flow readable: avoid multi-line ternaries when an `if` communicates intent more clearly.
- Eliminate low-signal noise: remove comments that merely state the obvious or “we’re not doing X”.
- Fix Flow properly instead of suppressing: add the needed Flow typings for callbacks rather than using `$FlowFixMe` when it’s avoidable.

Example (readability + strict style):
```js
// Prefer if over a multi-line ternary
let result;
if (cond) {
  result = a;
} else {
  result = b;
}

// Prefer shared helpers / strict equality
if (isArray(value) && x === y) {
  // ...
}
```