---
title: Prefer Self-Documenting Clarity
description: 'Write code that is readable and intention-revealing without relying
  on noisy comments or readability-hostile constructs.


  Guidelines:

  - Avoid comments that only restate what the code already demonstrates (remove “obvious”
  commentary; prefer code to explain intent).'
repository: facebook/react#b13
label: Code Style
language: JavaScript
comments_count: 7
repository_stars: 251894
---

Write code that is readable and intention-revealing without relying on noisy comments or readability-hostile constructs.

Guidelines:
- Avoid comments that only restate what the code already demonstrates (remove “obvious” commentary; prefer code to explain intent).
- Replace magic numbers with self-documenting expressions, e.g. use `someString.length` instead of hard-coded slice lengths.
- Use strict equality (`===`) unless a specific weak-equality case is required.
- Prefer consistent shared utilities/helpers (for example, use the project’s `isArray` helper rather than ad-hoc checks when that’s the established pattern).
- Prefer proper typing over suppressions like `$FlowFixMe` when the callback can be typed.
- Keep formatting simple: don’t use long multi-line ternaries; choose clear `if`/`else` or structured control flow. Avoid “boolean flag” control flow when an `else` branch yields clearer logic.

Example (slice self-documenting):
```js
// Prefer computed intent over magic constants + comments
if (name.startsWith('<anonymous>.')) {
  name = name.slice('<anonymous>.'.length);
}
```