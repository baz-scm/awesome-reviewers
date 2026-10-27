---
title: Avoid Wasted Computation
description: 'When optimizing performance, don’t just “delay” or “memoize” the result—ensure
  the expensive work is actually deferred or skipped.


  Apply this in two common places:'
repository: facebook/react#b13
label: Performance Optimization
language: TSX
comments_count: 2
repository_stars: 251893
---

When optimizing performance, don’t just “delay” or “memoize” the result—ensure the expensive work is actually deferred or skipped.

Apply this in two common places:

1) Prefer React deferral over custom debouncing (when appropriate)
- If the goal is to reduce perceived UI thrash during rapid updates, consider `useDeferredValue()` first.
- Use manual debouncing only when you can point to a specific bottleneck (e.g., frequent parse-error-driven state updates) that `useDeferredValue` doesn’t sufficiently mitigate. Ensure timers are properly cleaned up.

2) Filter/short-circuit before compute-heavy transforms
- Avoid patterns where heavy work still runs for every update and later gets ignored.
- Instead, narrow the data/inputs that you feed into expensive operations (e.g., tabification) before doing the work.

Example (skip work early instead of memoizing ignored UI):

```ts
// Instead of building/rendering all tabs then filtering,
// short-circuit before tabification/render prep.
for (const [passName, results] of compilerOutput.results) {
  if (!store.showInternals) {
    // Keep only the required passes
    if (passName !== 'Output' && passName !== 'SourceMap') continue;
  }

  // Now do the expensive work only for included passes
  // e.g., build tab content for this pass
}
```

Outcome: fewer redundant computations, less UI thrash during typing, and more predictable performance improvements.