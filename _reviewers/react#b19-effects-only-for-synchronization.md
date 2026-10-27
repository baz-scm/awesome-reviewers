---
title: Effects only for synchronization
description: Reserve `useEffect` for synchronizing with imperative/external systems
  (DOM APIs, subscriptions, scroll position, etc.) that can't be expressed as render
  output. Do not use effects to derive state from props/state that the UI should reflect
  immediately — compute it during render (or update state synchronously during render,
  which is safe and not "cascading"...
repository: facebook/react#b19
label: React
language: JavaScript
comments_count: 6
repository_stars: 251893
---

Reserve `useEffect` for synchronizing with imperative/external systems (DOM APIs, subscriptions, scroll position, etc.) that can't be expressed as render output. Do not use effects to derive state from props/state that the UI should reflect immediately — compute it during render (or update state synchronously during render, which is safe and not "cascading" the way an effect-driven update is) so the browser never paints a stale frame before the correction runs. For example, resetting a selection when a prop changes should be done with a render-time state comparison, not an effect:

```js
const [prevData, setPrevData] = useState(data);
if (prevData !== data) {
  setPrevData(data);
  selectIndex(data.length > 0 ? 0 : null);
}
```

When an effect is genuinely needed (e.g. calling an imperative API like `scrollToItem` to match derived state), keep it, but:
- Minimize its dependency array and extract event-handler-like logic that shouldn't retrigger the effect into `useEffectEvent`, so you don't tear down/rebuild subscriptions (e.g. `addEventListener`) on every unrelated state change.
- Document why the logic must live in an effect versus a handler or render, including any non-obvious guard conditions (e.g. why a particular dependency is checked but not read in the effect body).

For expensive derived computations (e.g. searching/filtering a large tree) triggered by fast user input, keep the input's own state update synchronous so typing never feels blocked, and defer the expensive derivation with `useDeferredValue` (or wrap it in `startTransition`) so it runs at lower priority. Surface pending state (`value !== deferredValue`) to show a loading indicator when the deferred work is still catching up, and benchmark against realistic data sizes to confirm the transition keeps the UI responsive.