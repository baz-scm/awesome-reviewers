---
title: Simplify control flow
description: 'Favor the simplest, most direct control-flow structure over constructs
  that add indirection or unnecessary branching. In practice this means:


  - Don''t add an `else` after a `return`/`throw` in the `if` branch; just fall through
  to the next statement.'
repository: facebook/react#b19
label: Code Style
language: JavaScript
comments_count: 5
repository_stars: 251893
---

Favor the simplest, most direct control-flow structure over constructs that add indirection or unnecessary branching. In practice this means:

- Don't add an `else` after a `return`/`throw` in the `if` branch; just fall through to the next statement.
- Avoid introducing a boolean flag solely to decide which cleanup/finalization code to run later; instead duplicate the few lines in each branch so the control flow stays explicit and linear.
- Avoid multi-line or deeply nested ternaries; if a ternary needs to span multiple lines for readability, switch to a plain `if`/`else`. For simple two-way choices, prefer a single-line ternary or template literal over a multi-step chain.
- Avoid wrapping a condition in a helper like `isSomething(value)` just to branch on it later; keep the switch/if that already drives control flow and dispatch directly from it, rather than scattering boolean-returning helpers that obscure the flow.

Example:

```js
// Avoid
if (cond) {
  return doA();
} else {
  return doB();
}

// Prefer
if (cond) {
  return doA();
}
return doB();
```

```js
// Avoid: flag just to control later behavior
let allComplete = false;
// ...sets allComplete somewhere...
if (allComplete) {
  completeWriting(destination);
  flushBuffered(destination);
} else {
  flushBuffered(destination);
}

// Prefer: duplicate the small branch-specific code
if (allComplete) {
  completeWriting(destination);
  flushBuffered(destination);
} else {
  flushBuffered(destination);
}
```

```js
// Avoid
const title = isProfiling
  ? `Stop profiling - ${shortcut}`
  : `Start profiling - ${shortcut}`;

// Prefer
const title = `${isProfiling ? 'Stop' : 'Start'} profiling - ${shortcut}`;
```

Keeping control flow flat and explicit makes code easier to follow, review, and modify, and avoids hidden state or abstractions that hide what the code actually does.</description>
</invoke>
