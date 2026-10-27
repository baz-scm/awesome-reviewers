---
title: Meaningful Name Minimalism
description: 'Use the smallest name that preserves meaning, and only rename/disambiguate
  when there’s a real semantic or syntax requirement.


  Apply:

  - Destructuring/rewrites: don’t alias to the same identifier.'
repository: facebook/react#b16
label: Naming Conventions
language: Markdown
comments_count: 4
repository_stars: 251891
---

Use the smallest name that preserves meaning, and only rename/disambiguate when there’s a real semantic or syntax requirement.

Apply:
- Destructuring/rewrites: don’t alias to the same identifier.
  - Prefer:
    - `const { disabled } = obj;`
    - `const { 'aria-label': ariaLabel } = props;` (quote keys that aren’t valid identifiers)
  - Avoid:
    - `const { disabled: disabled } = obj;`
    - `const { ariaLabel: ariaLabel } = props;` (when the source key is actually `aria-label`)
- Preserving function names: keep stable/original names whenever the function already has an intended name. Only generate “named” wrapper identifiers for cases that truly come from anonymous functions assigned to variables.
- Generated identifiers: avoid noisy, always-on components like `arg0` when they don’t add information. If there’s a known special/builtin pattern, name it without the index.
- Public/tool/API naming: keep common concepts consistent (e.g., “stack”), and add a suffix only to reflect a real difference in the returned data structure (e.g., “..._stack_trace” vs “..._stack”).

Example (destructuring):
```js
// Good
const { disabled } = t0;
const { 'aria-label': ariaLabel } = t0;

// Avoid
const { disabled: disabled } = t0;
const { ariaLabel: ariaLabel } = t0;
```