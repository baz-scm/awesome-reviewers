---
title: Prefer clear control flow
description: Write code so its intent is obvious through control flow and consistent
  style—avoid extra noise (redundant comments, unnecessary branches/helpers, hardcoded
  “magic” with misleading explanations), keep formatting readable, and don’t paper
  over missing types when straightforward.
repository: facebook/react#b4
label: Code Style
language: JavaScript
comments_count: 8
repository_stars: 251885
---

Write code so its intent is obvious through control flow and consistent style—avoid extra noise (redundant comments, unnecessary branches/helpers, hardcoded “magic” with misleading explanations), keep formatting readable, and don’t paper over missing types when straightforward.

Practical rules:
- Remove unnecessary `else` blocks after an early `return`.
  ```js
  if (condition) {
    return doA();
  }
  return doB();
  ```
- Don’t add comments that restate the obvious (e.g., “don’t return early” when there’s no return). Use comments only for non-obvious intent, invariants, or tricky rationale.
- Prefer expressions over magic numbers with explanatory comments (e.g., compute lengths):
  ```js
  name = name.slice('<anonymous>.'.length);
  ```
- Use strict equality (`===` / `!==`) unless weak equality is explicitly required.
- Keep formatting readable: avoid huge multi-line ternaries; use `if`/statements instead.
- Prefer proper local typings/annotations over `// $FlowFixMe[missing-local-annot]` when you can add the correct function/parameter types.

Outcome: code that’s easier to scan, less error-prone, and more maintainable across the team.