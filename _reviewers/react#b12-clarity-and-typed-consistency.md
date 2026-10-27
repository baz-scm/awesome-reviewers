---
title: Clarity and Typed Consistency
description: 'Adopt a “clarity + consistency + real typing” standard:


  - Remove noise: don’t keep comments that merely restate what the code already does
  (e.g., “don’t return early” when control flow already makes that obvious).'
repository: facebook/react#b12
label: Code Style
language: JavaScript
comments_count: 7
repository_stars: 251896
---

Adopt a “clarity + consistency + real typing” standard:

- Remove noise: don’t keep comments that merely restate what the code already does (e.g., “don’t return early” when control flow already makes that obvious).
- Eliminate dead code: remove unused variables even if lint misses them in test files.
- Prefer strict equality: use `===`/`!==` by default unless there’s a documented reason to use weak equality.
- Don’t use FlowFixMe for missing callback annotations: if a callback needs typing, add the correct Flow annotation instead of `// $FlowFixMe[missing-local-annot]`.
- Keep feature gating readable: gate with the feature flag at the outer level instead of deeply nesting extra checks.
- Avoid hard-to-read ternaries: don’t use multi-line ternaries for control flow—use `if`.

Example (Flow callback typing instead of FlowFixMe):

```js
// Bad style (papering over missing local types)
// $FlowFixMe[missing-local-annot]
const handleIndexChange = ({currentTarget}) => {
  const raw = currentTarget.value;
  // ...
};

// Preferred style (explicit local types)
const handleIndexChange = (
  event: SyntheticInputEvent<HTMLInputElement>,
) => {
  const raw = event.currentTarget.value;
  // ...
};
```