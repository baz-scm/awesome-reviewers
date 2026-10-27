---
title: Avoid unnecessary effects
description: 'Several reviews flagged `useEffect` being used as an escape hatch for
  state that can be derived or updated synchronously. Before reaching for `useEffect`,
  check whether the logic belongs in the render body, in the event handler that triggers
  the change, or in a `useMemo`/derived value instead:'
repository: facebook/react#b20
label: React
language: JavaScript
comments_count: 10
repository_stars: 251895
---

Several reviews flagged `useEffect` being used as an escape hatch for state that can be derived or updated synchronously. Before reaching for `useEffect`, check whether the logic belongs in the render body, in the event handler that triggers the change, or in a `useMemo`/derived value instead:

- Derived state (state that is purely a function of other state/props) should be computed during render or in the state setter/event handler that caused the change, not synchronized afterward in an effect. Writing to state (or refs) "to adjust it when a prop/other state changes" in an effect causes an extra render where the UI can briefly show stale data, since effects run after paint. Doing it during render avoids that flicker and the extra commit-then-effect round trip. Example: instead of
```js
useEffect(() => {
  if (commitData !== prevCommitData) {
    setPrevCommitData(commitData);
    selectCommitIndex(commitData.length > 0 ? 0 : null);
  }
}, [commitData]);
```
prefer updating during render:
```js
const [prevCommitData, setPrevCommitData] = useState(commitData);
if (prevCommitData !== commitData) {
  setPrevCommitData(commitData);
  selectCommitIndex(commitData.length > 0 ? 0 : null);
}
```
Calling `setState` during render like this is not a "cascading update" in the problematic sense — it's applied immediately in the same render pass, unlike state changes scheduled from an effect after commit.
- When a state change is driven by a specific user action (e.g. starting profiling, changing a filter, submitting a search), perform the related updates directly inside that action's callback/handler rather than reacting to the resulting state change in an effect. This keeps related updates batched and makes the causality explicit.
- For expensive derived computations that shouldn't block an input update, keep the controlled input state update synchronous and compute the derived result from a `useDeferredValue` of that state (or wrap the computation in `startTransition`), rather than computing it in an effect. Expose a `pending` flag (`value !== deferredValue`) if you need to show a loading indicator for the deferred work.
- Reserve `useEffect`/`useLayoutEffect` for true synchronization with systems outside React's render (DOM APIs, subscriptions, imperative widgets like `scrollToItem`). Even then, minimize dependencies: wrap values that shouldn't trigger re-subscription (e.g. a callback that only needs the latest state at call time) in `useEffectEvent` instead of adding them to the dependency array, to avoid tearing down and re-creating listeners on every change.
- When genuinely synchronizing scroll position/focus with layout, consider `useLayoutEffect` instead of `useEffect` if a one-frame visual desync is observable.

Applying this consistently reduces redundant renders, eliminates "flash of stale UI" bugs, and makes it clear whether a given state update is a render-time derivation, an event-driven side effect, or a true synchronization with the outside world.