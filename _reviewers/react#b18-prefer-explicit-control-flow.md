---
title: Prefer explicit control flow
description: 'Favor straightforward, explicit control structures over indirect or
  clever constructs that obscure intent. Specifically:


  - Avoid introducing boolean "flag" variables purely to alter behavior after a loop
  or block; instead, duplicate the small amount of code in each branch so the control
  flow is visible at a glance (e.g., call...'
repository: facebook/react#b18
label: Code Style
language: JavaScript
comments_count: 4
repository_stars: 251889
---

Favor straightforward, explicit control structures over indirect or clever constructs that obscure intent. Specifically:

- Avoid introducing boolean "flag" variables purely to alter behavior after a loop or block; instead, duplicate the small amount of code in each branch so the control flow is visible at a glance (e.g., call `completeWriting`/`flushBuffered` directly in both the "finished" and "not finished" branches rather than toggling an `allComplete` flag).
- Avoid scattering `isSomething(...)` predicate helpers through a function to fork behavior; prefer a single switch/if structure where each branch already determines the next action, and add new branches there instead of layering conditionals on top of existing flow.
- Keep conditional expressions simple—long or multi-line ternaries should be rewritten as `if`/`else` for readability.
- Prefer self-documenting values over magic numbers with explanatory comments. For example, use `name.slice('<anonymous>.'.length)` instead of `name.slice(12)` plus a comment explaining why 12 was chosen; the literal is inlined at build time, so there's no runtime cost.

These practices keep code paths easy to trace and reduce the cognitive overhead of cross-referencing flags, helper predicates, or magic constants.