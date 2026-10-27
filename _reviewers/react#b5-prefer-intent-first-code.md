---
title: Prefer Intent-First Code
description: 'Write code and tests that are readable and resilient: communicate intent
  in code, avoid low-value or redundant comments, and prefer clear idiomatic patterns
  over formatting shortcuts or suppression directives.'
repository: facebook/react#b5
label: Code Style
language: JavaScript
comments_count: 6
repository_stars: 251886
---

Write code and tests that are readable and resilient: communicate intent in code, avoid low-value or redundant comments, and prefer clear idiomatic patterns over formatting shortcuts or suppression directives.

Guidelines:
- Prefer intent-level assertions: avoid encoding framework internals/markers in test expectations; use direct, behavior-focused checks (e.g., visibility/state), so assertions are easy to scan and less brittle.
- Remove “noise comments”: don’t comment things that the code already makes obvious (e.g., “don’t return early” when control flow clearly falls through). Use comments only for non-obvious intent/why.
- Avoid magic numbers when the source is available (e.g., use `'<anonymous>.'.length` rather than a hard-coded length with a comment).
- Enforce JS idioms consistently: use strict equality (`===`/`!==`) unless there’s a deliberate reason for weak equality.
- Prefer proper typing over suppressions: if Flow lacks inference for a callback, add Flow typings rather than `$FlowFixMe`.
- Keep formatting readable: if an expression spans many lines (e.g., a long ternary), refactor to `if`.

Example patterns:
```js
// Prefer derived lengths
name = name.slice('<anonymous>.'.length);

// Prefer if over long ternaries
let indexValue;
if (indexDraft !== null) {
  indexValue = indexDraft;
} else {
  indexValue = String(currentResultNumber);
}
```