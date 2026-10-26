---
title: Prefer idiomatic, typed code
description: 'Write code that is consistent with existing project idioms, is readable
  at a glance, and is properly typed.


  Apply these style rules:

  1) Avoid magic numbers + redundant comments'
repository: facebook/react#b3
label: Code Style
language: JavaScript
comments_count: 6
repository_stars: 251883
---

Write code that is consistent with existing project idioms, is readable at a glance, and is properly typed.

Apply these style rules:
1) Avoid magic numbers + redundant comments
- If you’re slicing by a prefix length, use the source string’s `.length` rather than hardcoding and commenting the discrepancy.
- Don’t add comments that simply restate obvious control flow (“don’t return early” when no return exists).

2) Prefer real Flow types over `$FlowFixMe`
- For newly added callbacks, add local parameter typings so Flow can verify the code.

3) Use project-consistent helpers/utilities
- Prefer existing helpers (e.g., `isArray`) over ad-hoc checks when the project has a standard, including for Flow-related correctness/abstractions.

4) Keep expressions readable
- Avoid dense multi-line ternaries when an `if` improves clarity.

5) Default to strict equality
- Use `===` / `!==` unless there is a documented, specific reason for loose equality.

Example (types + no FlowFixMe):
```js
// Instead of:
// // $FlowFixMe[missing-local-annot]
// const handleIndexChange = ({currentTarget}) => { ... }

type CurrentTarget = {value: string, select: () => void};

const handleIndexChange = (event: {
  currentTarget: CurrentTarget,
}) => {
  const raw = event.currentTarget.value;
  // ...
};
```

Example (no magic number):
```js
name = name.slice('<anonymous>.'.length);
```