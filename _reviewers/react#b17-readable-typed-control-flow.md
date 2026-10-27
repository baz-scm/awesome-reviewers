---
title: Readable, Typed Control Flow
description: 'Maintain consistent, readable code by: (1) preferring straightforward
  control flow over clever/indirect constructs, (2) using strict equality consistently,
  (3) removing style-noise comments and unnecessary `$FlowFixMe` directives, and (4)
  keeping Flow types complete (especially for event/callback handlers).'
repository: facebook/react#b17
label: Code Style
language: JavaScript
comments_count: 11
repository_stars: 251891
---

Maintain consistent, readable code by: (1) preferring straightforward control flow over clever/indirect constructs, (2) using strict equality consistently, (3) removing style-noise comments and unnecessary `$FlowFixMe` directives, and (4) keeping Flow types complete (especially for event/callback handlers).

Guidelines
- Use strict equality (`===`) unless you have an explicit, justified reason for weak equality.
- Avoid multiline ternaries; use `if/else` for readability.
- Avoid boolean/flag variables when simple control flow (duplicate the small branches) is clearer.
- Ensure `if/else if` branches match the intent—avoid structures that look like they might run multiple paths when they won’t.
- Don’t add “obvious intent” comments (e.g., commenting that control will fall through); remove them when the code already demonstrates behavior.
- Don’t rely on `$FlowFixMe[missing-local-annot]` for callback typing—add proper local annotations instead.
- Prefer shared helper utilities (e.g., `isArray`) when the project already has them, for consistency/typing.

Examples
- Replace FlowFixMe with a typed callback:
  ```js
  // Bad
  // $FlowFixMe[missing-local-annot]
  const handleKeyDown = event => { /* ... */ };

  // Good
  type KeyboardEvent = SyntheticKeyboardEvent<HTMLElement>;
  const handleKeyDown = (event: KeyboardEvent) => { /* ... */ };
  ```

- Replace a large multiline ternary with `if`:
  ```js
  // Bad
  const v = cond ? firstValue :
    secondValue;

  // Good
  let v;
  if (cond) v = firstValue;
  else v = secondValue;
  ```

- Use strict equality and shared helpers:
  ```js
  if (value === null) return;
  if (isArray(value)) { /* ... */ }
  ```