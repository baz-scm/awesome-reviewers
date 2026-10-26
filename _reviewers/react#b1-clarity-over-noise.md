---
title: Clarity Over Noise
description: 'Adopt a readability-first standard: prefer obvious control flow, simple
  gating, and correct typing over comments, flags, and formatting tricks that obscure
  intent.'
repository: facebook/react#b1
label: Code Style
language: JavaScript
comments_count: 9
repository_stars: 251878
---

Adopt a readability-first standard: prefer obvious control flow, simple gating, and correct typing over comments, flags, and formatting tricks that obscure intent.

Apply:
- Remove low-value “we’re not doing X” comments when control flow already makes the behavior clear.
- Don’t add redundant condition checks (e.g., `isPreambleInsertion(...)`) when the code structure already guarantees the state; refactor so only the necessary branching remains.
- Avoid multi-line ternary expressions; prefer `if`/early returns for legibility.
- Use strict equality (`===`) unless there’s a deliberate reason for weak equality.
- Prefer proper Flow typings for callbacks over `$FlowFixMe` suppressions.
- Keep feature-flag gating shallow and non-redundant (gate at the top level before doing specialized work), so nested conditionals don’t hide what will run.

Example (avoid long ternary / prefer `if`):
```js
// Bad (wide ternary)
const x = condition ? foo : bar;

// Good
let x;
if (condition) {
  x = foo;
} else {
  x = bar;
}
```

Example (prefer strict equality):
```js
// Bad (unless you truly need it)
if (value == null) {}

// Good
if (value === null || value === undefined) {}
```