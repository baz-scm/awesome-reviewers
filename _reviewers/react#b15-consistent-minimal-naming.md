---
title: Consistent Minimal Naming
description: Use names/labels that are semantically accurate, stable, and not noisier
  than necessary—especially for derived identifiers, API/tool names, and structured
  keys.
repository: facebook/react#b15
label: Naming Conventions
language: Markdown
comments_count: 4
repository_stars: 251891
---

Use names/labels that are semantically accurate, stable, and not noisier than necessary—especially for derived identifiers, API/tool names, and structured keys.

Applied rules:
- Avoid needless renames: don’t change `disabled: disabled` → `disabled`; prefer shorthand.
- Destructure special keys correctly: use quoted property names for keys like `aria-label`.
- Preserve meaningful existing identifiers: if a function is already named, keep its name; only apply renaming/wrapping when the original was anonymous.
- Keep terminology stable across related concepts: if the team already uses “stack”, don’t introduce a parallel “branch” term for a different return shape—use consistent base terms plus suffixes to disambiguate.
- Minimize generated label noise: omit redundant indices/markers (e.g., don’t emit `arg0` when a special case can be unambiguous; include indices only when they’re needed to differentiate multiple anonymous arguments).

Example (destructuring special keys + minimal identifiers):
```js
// Prefer shorthand for standard identifiers
const { disabled } = props;

// Use quoted keys for special property names
const { 'aria-label': ariaLabel } = props;
```

Outcome: code and generated artifacts are easier to read, diff, and reason about because naming stays consistent and avoids unnecessary variation.