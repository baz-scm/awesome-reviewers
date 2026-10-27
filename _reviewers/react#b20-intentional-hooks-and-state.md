---
title: Intentional hooks and state
description: When using hooks like `useEffect`, `useMemo`, or custom state logic,
  favor built-in React mechanisms and keep the implementation minimal and purposeful
  rather than adding ad-hoc workarounds.
repository: facebook/react#b20
label: React
language: TSX
comments_count: 4
repository_stars: 251895
---

When using hooks like `useEffect`, `useMemo`, or custom state logic, favor built-in React mechanisms and keep the implementation minimal and purposeful rather than adding ad-hoc workarounds.

- Before writing manual timers or debouncing logic with `useRef`/`setTimeout`, check if a built-in primitive like `useDeferredValue` already solves the problem. Only add custom debouncing if the built-in mechanism truly isn't sufficient (e.g. it updates too eagerly for your UX needs), and document why.
- Only add cleanup logic in `useEffect` when there's a real resource or side effect that needs to be released (e.g. subscriptions, intervals, listeners that outlive the component). A `setTimeout` whose callback naturally expires and doesn't mutate external state after unmount usually doesn't need a cleanup effect — weigh whether the unmounted callback could cause a bug before adding the extra effect.
- Don't memoize or pre-process data (e.g. with `useMemo`) if the surrounding code already avoids the expensive work, or if memoizing doesn't actually prevent the costly computation. For example, instead of computing all tab content and then filtering it in a `useMemo`, skip the expensive work for hidden tabs entirely:

```js
for (const [passName, results] of compilerOutput.results) {
  if (!store.showInternals && passName !== 'Output' && passName !== 'SourceMap') {
    continue; // skip building content for tabs that won't be shown
  }
  // ...
}
```

- When resetting or clearing component/store state (e.g. a "force reset" action), make the behavior complete and predictable rather than selectively preserving some fields. If a reset is meant to clear all client state, don't special-case persisting unrelated fields like `showInternals` — that erodes the guarantee that "reset" means a clean slate.

Applying this standard keeps hook usage minimal, avoids unnecessary re-renders or stale closures, and makes state transitions easier to reason about.