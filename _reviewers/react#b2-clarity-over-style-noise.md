---
title: Clarity Over Style Noise
description: 'Write code that is easy to read, consistent with project conventions,
  and type-correct—avoid “noise” that repeats the obvious.


  Apply these rules:

  - Don’t add comments that restate the obvious control flow (delete comments like
  “don’t return early” when the code already makes it clear).'
repository: facebook/react#b2
label: Code Style
language: JavaScript
comments_count: 8
repository_stars: 251882
---

Write code that is easy to read, consistent with project conventions, and type-correct—avoid “noise” that repeats the obvious.

Apply these rules:
- Don’t add comments that restate the obvious control flow (delete comments like “don’t return early” when the code already makes it clear).
- Prefer team conventions over ad-hoc equivalents:
  - Use strict equality unless there’s a specific reason for weak equality.
  - Use shared helpers for consistency (e.g., an imported `isArray` helper instead of `Array.isArray` when that’s the project convention).
- Fix Flow properly: if a callback needs an annotation, add the Flow types instead of using `$FlowFixMe`.
- Keep feature-flag branching structured so callers don’t need redundant predicate checks—put the guarantee in a helper and let control flow handle the variant behavior.
- Prefer readable formatting:
  - Avoid multi-line ternaries when a simple `if` is clearer.

Example patterns:
```js
// Prefer strict equality
if (x === null) { ... }

// Avoid redundant FixMe when you can type
// $FlowFixMe[missing-local-annot] const onChange = ...
const onChange = (e: SyntheticEvent<HTMLInputElement>) => {
  const raw = e.currentTarget.value;
};

// Avoid style-noise comment
// (Remove comments that just restate what the code already does)

// Prefer readable branching over hard-to-scan ternaries
if (!Fp.bind) {
  // ...
}
```

The result should be code that communicates intent without extra commentary, matches existing idioms, and doesn’t bypass type checks.