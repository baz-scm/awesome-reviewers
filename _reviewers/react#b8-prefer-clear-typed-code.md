---
title: Prefer Clear, Typed Code
description: "Write code that is easy to scan and hard to misread:\n\n- Prefer explicit\
  \ control flow over clever/opaque patterns.\n  - Avoid multiline ternaries; use\
  \ `if`."
repository: facebook/react#b8
label: Code Style
language: JavaScript
comments_count: 5
repository_stars: 251889
---

Write code that is easy to scan and hard to misread:

- Prefer explicit control flow over clever/opaque patterns.
  - Avoid multiline ternaries; use `if`.
  - Prefer branching to state flags when it improves clarity.
- Keep formatting readable.
  - Don’t use “clever” expressions that spread across many lines.
- Use consistent correctness styles.
  - Prefer strict equality (`===`) unless there’s a clear reason for weak equality.
  - Reuse existing helpers/utilities for common checks to match local conventions.
- Avoid style-noise during refactors.
  - Don’t add comments that merely restate what the code already obviously does (e.g., “don’t return early” when there is no early return).
- Don’t paper over typing problems.
  - Prefer adding proper Flow typings over `FlowFixMe` when feasible.

Example (avoid multiline ternary):
```js
// Avoid:
const x = condition
  ? doA()
  : doB();

// Prefer:
let x;
if (condition) {
  x = doA();
} else {
  x = doB();
}
```