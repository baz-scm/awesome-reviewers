---
title: Explicit state over inference
description: Don't infer transient UI state (a new turn started, a message was sent,
  fetched data is fresh, a resource was reaped) by comparing counts, diffs, or snapshots
  across renders. These heuristics break under reordering, concurrent async results,
  or hydration, as seen with a "run count" check that failed to detect a new turn,
  and a userMessageCount comparison...
repository: 'cline/cline#

  zzprobe3b82974b: x'
label: React
language: TSX
comments_count: 8
repository_stars: 71067
---

Don't infer transient UI state (a new turn started, a message was sent, fetched data is fresh, a resource was reaped) by comparing counts, diffs, or snapshots across renders. These heuristics break under reordering, concurrent async results, or hydration, as seen with a "run count" check that failed to detect a new turn, and a userMessageCount comparison that misread session-history hydration as a user send. Instead, track the transition explicitly at its source: bump an epoch/generation value when the real event occurs, or pass down an explicit flag (e.g. `isSessionSwitching`) from the component that actually knows the context, and compare against that.

This matters even more for components that can be hidden and shown again without unmounting (e.g. React's `Activity`, or StrictMode's double-invoke of effects): effects rerun on show, so any "run once" gate stored in `useState` will be lost and misfire again. Use a `ref` for one-time bootstrap gates, since refs survive a hide/show cycle, while still refreshing data that should update on every show. Conversely, any cleanup that only runs on a true unmount (timers, recording flags, in-flight cancellations) must also run — or be mirrored — when a keep-alive component is hidden, otherwise state like `isListening` will desync from reality until the next real unmount.

Example pattern for a one-time bootstrap that must survive Activity hiding, but still refresh on every successful load:
```ts
const hasBootstrapped = useRef(false);
useEffect(() => {
  loadContext().then((ctx) => {
    refreshEnvironment(ctx); // always refresh
    if (!hasBootstrapped.current) {
      hasBootstrapped.current = true;
      dispatch({ type: "select-environment-draft" }); // only once
    }
  });
}, []);
```
When a derived boolean is needed (e.g. "is this diff still for the latest turn?"), prefer having the data-fetching hook report an explicit `current`/`fresh` flag tied to a refresh key, rather than re-deriving it from unrelated counters.