---
title: Render purity and deferral
description: 'Keep render functions pure and push side-effectful or expensive work
  to the right place:


  1. Never read or write a mutable ref during render. Refs should only be read/written
  inside effects or event handlers; reading a ref''s current value while rendering
  breaks React''s rendering guarantees and can cause stale or inconsistent UI. If
  render needs to fall back...'
repository: facebook/react#b18
label: React
language: TSX
comments_count: 4
repository_stars: 251889
---

Keep render functions pure and push side-effectful or expensive work to the right place:

1. Never read or write a mutable ref during render. Refs should only be read/written inside effects or event handlers; reading a ref's current value while rendering breaks React's rendering guarantees and can cause stale or inconsistent UI. If render needs to fall back to a previous value (e.g., keeping the last valid formatted output when new input is invalid), compute and store that value in an effect/reducer instead of dereferencing a ref inline during render.

2. Prefer React's built-in scheduling primitives over hand-rolled timers for deferring expensive updates. Use `useDeferredValue` (or transitions) instead of manual `setTimeout`-based debouncing when the goal is just to avoid re-rendering too often. Only introduce manual timers when you need custom debounce semantics, and only add a cleanup effect for them if the timer manages a resource that would otherwise leak or cause an unwanted side effect after unmount (e.g., an interval or subscription). A one-shot timeout whose only effect is a state dispatch after unmount usually does not need explicit cleanup — reason about whether the pending callback can cause harm before adding cleanup code reflexively.

3. When optimizing rendering, remove unnecessary work instead of filtering it after the fact. For example, rather than building a full list of tab components and then memoizing a filtered subset, skip generating the unneeded items up front:

```js
for (const [passName, results] of compilerOutput.results) {
  if (store.showInternals === false && passName !== 'Output' && passName !== 'SourceMap') {
    continue;
  }
  // only do the work for tabs you actually need
}
```

Avoid adding `useMemo` purely out of habit — measure whether the computation is actually expensive before memoizing, and prefer eliminating redundant work entirely over wrapping it in memoization.