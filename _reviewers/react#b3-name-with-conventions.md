---
title: Name With Conventions
description: Use established naming conventions and ensure identifiers encode precise
  semantics—especially for public APIs, semi-public types, user-visible labels, and
  state/contract-sensitive flags.
repository: facebook/react#b3
label: Naming Conventions
language: JavaScript
comments_count: 9
repository_stars: 251883
---

Use established naming conventions and ensure identifiers encode precise semantics—especially for public APIs, semi-public types, user-visible labels, and state/contract-sensitive flags.

Guidelines:
- Match the *meaning* of the value: “was”/“is” should reflect history vs current state; “hint” should describe a target/heuristic, not a max.
- Follow existing patterns: option types should follow the established `${ucfirst(methodName)}Options` (and consider exporting/aliasing if names are semi-public).
- Keep naming normalization centralized: if a prefix like `top` is just a transport detail, remove/normalize it at the source to prevent duplicated downstream checks.
- Preserve compatibility for public names: introduce the new name, and alias the old one (e.g., export `Activity` while keeping `unstable_Activity` as an alias).
- Ensure consistency with related identifiers: static flags and other patterned names should follow the same suffix/prefix rules unless there’s a documented exception.
- For user-visible strings (e.g., devtools): prefer naming that matches expected user mental models, while staying consistent with existing logic.

Example (semantic guard naming):
```js
// Prefer history-based naming when the behavior triggers at hide-time
if (!offscreenSubtreeWasHidden) {
  unmountHoistable(deletedFiber.stateNode);
}
```

Example (public API rename with compatibility):
```js
export {Activity, Activity as unstable_Activity};
```