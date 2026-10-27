---
title: Code Clarity Standards
description: 'When improving code style, prioritize readability that is enforced by
  code (not comments) and keep Flow typing and idioms consistent.


  Guidelines:

  - Prefer self-documenting expressions over explanatory comments with fixed assumptions
  (e.g., compute lengths via `''<anonymous>.''.length` rather than a magic number
  plus a comment).'
repository: facebook/react#b9
label: Code Style
language: JavaScript
comments_count: 7
repository_stars: 251891
---

When improving code style, prioritize readability that is enforced by code (not comments) and keep Flow typing and idioms consistent.

Guidelines:
- Prefer self-documenting expressions over explanatory comments with fixed assumptions (e.g., compute lengths via `'<anonymous>.'.length` rather than a magic number plus a comment).
- Avoid low-signal comments that state the obvious (e.g., “don’t return early” when control flow already makes it clear). If a comment doesn’t add intent, delete it.
- Use readable branching over hard-to-scan formatting (avoid long multi-line ternaries; use `if`/early returns as appropriate).
- Follow repo idioms for correctness/consistency: prefer strict equality (`===`) unless there’s a specific, documented reason not to.
- Reuse existing utility helpers for common operations where the codebase provides them (e.g., prefer `isArray(value)` over ad-hoc checks when that’s the standard).
- Add proper Flow types for callback params and event handlers; don’t use `$FlowFixMe[missing-local-annot]` when simple local typings are possible.

Example (patterned after the discussions):
```js
// Prefer idiomatic helpers / strict equality
import {isArray} from 'shared/something';

if (value === undefined) return;
if (isArray(value)) {
  // ...
}

// Avoid redundant “obvious” comments; prefer self-documenting expressions
name = name.slice('<anonymous>.'.length);

// Avoid missing-local-annot suppressions
// $FlowFixMe[missing-local-annot] (avoid)
const handleKeyDown = (event: KeyboardEvent) => {
  if (event.key === 'Enter' || event.key === ' ') {
    // ...
  }
};
```

Adopting this will reduce diff noise, improve scan-ability, and keep Flow suppressions to cases where they’re genuinely required.