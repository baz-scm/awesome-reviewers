---
title: Prefer Clear Control Flow
description: 'When writing or refactoring code, optimize for readability and intention:

  - Use explicit control flow instead of boolean flags (duplicate small code paths
  if needed).'
repository: facebook/react#b14
label: Code Style
language: JavaScript
comments_count: 7
repository_stars: 251893
---

When writing or refactoring code, optimize for readability and intention:
- Use explicit control flow instead of boolean flags (duplicate small code paths if needed).
- Avoid large/complex ternaries across many lines; prefer `if`.
- Don’t build extra indirection just to encode conditions (e.g., avoid sprinkling `isSomething(...)` checks when the existing control-flow (like a `switch`) can route directly to specialized logic).
- Remove redundant comments that merely restate what the code clearly does.
- Prefer strict equality (`===`) unless weak equality is genuinely required.
- Don’t hide missing types with suppressions (e.g., avoid `$FlowFixMe` when you can add proper Flow types).
- Keep utilities cohesive: organize code by feature/domain rather than accumulating unrelated “utils” dumping grounds.

Example (avoid flag + multiline ternary + redundant comment):
```js
// Prefer direct branches over a boolean flag
try {
  if (shouldFinish) {
    complete();
    flush();
  } else {
    complete();
    flush();
  }
} finally {
  // no redundant comments about what isn't happening
}

// Prefer if over multiline ternary
let value;
if (draft != null) {
  value = draft;
} else {
  value = String(count);
}

// Avoid Flow suppression by typing instead of $FlowFixMe
function onChange({currentTarget}: {currentTarget: HTMLInputElement}) {
  setValue(currentTarget.value);
}
```
