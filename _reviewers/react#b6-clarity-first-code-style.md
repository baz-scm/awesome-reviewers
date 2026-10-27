---
title: Clarity-First Code Style
description: 'Adopt a clarity-first code style that makes intent obvious and avoids
  formatting/type shortcuts.


  **Rules**

  - **Prefer clear control flow over redundant condition helpers/flags.** If a helper/switch
  already guarantees behavior, don’t re-check with extra `isSomething(...)` logic;
  don’t introduce boolean flags when straightforward branching is clearer.'
repository: facebook/react#b6
label: Code Style
language: JavaScript
comments_count: 6
repository_stars: 251888
---

Adopt a clarity-first code style that makes intent obvious and avoids formatting/type shortcuts.

**Rules**
- **Prefer clear control flow over redundant condition helpers/flags.** If a helper/switch already guarantees behavior, don’t re-check with extra `isSomething(...)` logic; don’t introduce boolean flags when straightforward branching is clearer.
- **Remove low-value comments.** Don’t comment on what the code already makes evident (e.g., “don’t return early” when the control flow already falls through).
- **Default to strict equality.** Use `===`/`!==` unless there is a documented, specific reason for weak equality.
- **Avoid `$FlowFixMe` when proper typings are easy.** Add Flow types for callback parameters/events rather than suppressing.
- **Keep formatting readable.** Avoid multi-line ternaries that span many lines; use `if`/early returns instead.
- **Use shared utilities/patterns for consistency** (e.g., prefer the project’s imported helper when available).

**Example (ternary -> if, and strict equality)**
```js
// Bad (hard to read)
const label = condition
  ? someVeryLongValue
  : otherVeryLongValue;

// Good
let label;
if (condition) {
  label = someVeryLongValue;
} else {
  label = otherVeryLongValue;
}

// Prefer strict equality
if (value === null) {
  // ...
}
```

Apply these consistently in reviews to reduce noise, improve maintainability, and keep behavior and types trustworthy.