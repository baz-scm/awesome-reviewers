---
title: Write Intent-Revealing Style
description: 'Adopt a style of code that makes intent obvious and avoids “papering
  over” issues with comments or suppressions.


  **Guidelines**

  1. **Don’t add comments that restate obvious behavior.** Only comment non-obvious
  intent/constraints; otherwise rely on clear control flow.'
repository: facebook/react#b16
label: Code Style
language: JavaScript
comments_count: 10
repository_stars: 251891
---

Adopt a style of code that makes intent obvious and avoids “papering over” issues with comments or suppressions.

**Guidelines**
1. **Don’t add comments that restate obvious behavior.** Only comment non-obvious intent/constraints; otherwise rely on clear control flow.
2. **Derive values directly from constants instead of adding correctness-prompts.** If you can compute a length/offset from a string, do it.
3. **Use repo conventions consistently:**
   - Prefer **strict equality** (`===`) unless there’s a concrete, justified reason.
   - Prefer **shared helpers** (e.g., `isArray`) over native checks when the codebase already has a convention.
4. **Prefer explicit local Flow typings over `$FlowFixMe[missing-local-annot]`.** Add callback parameter annotations (or inline typed destructuring) rather than suppressing.
5. **Favor readable control flow over complex expressions/duplicate condition helpers:**
   - Avoid large multi-line ternaries; use `if`.
   - Once a helper guarantees a property (e.g., “this is preamble”), don’t repeat redundant feature-flag/condition checks elsewhere.
6. **Keep new utilities/logic organized by feature/ownership, not in a generic dumping ground.**

**Mini examples**
```js
// Prefer derived constants over explanatory comments
if (name.startsWith('<anonymous>.')) {
  name = name.slice('<anonymous>.'.length);
}

// Prefer explicit Flow callback typing over FlowFixMe
// $FlowFixMe[missing-local-annot] // avoid
const handleKeyDown = (event: KeyboardEvent) => {
  if (event.key === 'Enter' || event.key === ' ') {
    if (event.key === ' ') event.preventDefault();
    toggleCollapsedVal();
  }
};

// Prefer if over long ternary
let shouldPolyfillBind = false;
if (!Function.prototype.bind) {
  shouldPolyfillBind = true;
}

// Prefer a helper that guarantees context over redundant checks
function pushStartHead(target, preamble, props) {
  // Here we already know it's a head preamble insertion
  target = enableFloat ? ((preamble: any)) : target;
  return pushStartGenericElement(target, 'head', props);
}
```