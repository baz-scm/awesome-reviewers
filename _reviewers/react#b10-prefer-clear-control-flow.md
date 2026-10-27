---
title: Prefer clear control flow
description: 'Adopt a style that keeps logic obvious, typed, and consistent. In practice:


  - Use strict equality (`===`) unless weak equality is required for a specific documented
  reason.'
repository: facebook/react#b10
label: Code Style
language: JavaScript
comments_count: 9
repository_stars: 251894
---

Adopt a style that keeps logic obvious, typed, and consistent. In practice:

- Use strict equality (`===`) unless weak equality is required for a specific documented reason.
- Prefer explicit control flow over “condition-abstraction” layers and temporary flags when they reduce clarity. If a helper name already implies the branch context, avoid re-checking the condition.
  - Also avoid adding boolean flags (e.g., `allComplete`) when simple branching/duplicating a small block is clearer.
- Avoid redundant comments that restate what the code already guarantees.
- Keep formatting readable: don’t use multi-line ternaries when a simple `if` reads better.
- Prefer correct Flow typings for callbacks and parameters; avoid `$FlowFixMe[missing-local-annot]` when a proper local annotation or typed parameter works.
- For consistency, use existing shared helpers (e.g., `isArray`) when they exist for style/Flow reasons.

Example pattern:
```js
type Props = { onKeyDown: (e: SyntheticKeyboardEvent<>) => void };

function handleKeyDown(event: SyntheticKeyboardEvent<>) {
  if (event.key === 'Enter' || event.key === ' ') {
    if (event.key === ' ') event.preventDefault();
    // ...
  }
}
```
(Use `===`, type callbacks instead of `$FlowFixMe[missing-local-annot]`, and keep branching straightforward.)