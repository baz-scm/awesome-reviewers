---
title: Manage Async Lifecycles
description: Async code must explicitly manage both (1) *when* work runs (priority/scheduling)
  and (2) *how long* it stays wired to resources (listener/state lifetimes), to prevent
  blocking, races, and memory retention.
repository: facebook/react#b6
label: Concurrency
language: JavaScript
comments_count: 5
repository_stars: 251888
---

Async code must explicitly manage both (1) *when* work runs (priority/scheduling) and (2) *how long* it stays wired to resources (listener/state lifetimes), to prevent blocking, races, and memory retention.

Apply these rules:

1) Detach on terminal conditions
- If you attach event listeners (e.g., to AbortSignal), ensure they’re removed when the request/render reaches a terminal status.
- Never keep large request objects reachable longer than necessary.

2) Compute expensive derived data at lower priority
- Keep controlled/urgent UI updates synchronous.
- Defer expensive derived computations (like searching a large tree) so they don’t block user input.

3) Centralize microtask/work scheduling behind an abstraction
- Provide a single scheduling API that can fall back safely (e.g., when queueMicrotask isn’t available).
- Avoid ad-hoc sync implementations that later introduce timing/ordering gaps.

4) Guard against overlapping/nested async renders
- Shared mutable module/global state used during rendering must be save/restore capable (or otherwise isolated per request).
- Assume nested renders can interleave and corrupt shared variables.

Example patterns:

- AbortSignal attach/detach:
```js
export function attachAbortSignal(request, signal) {
  if (signal.aborted) {
    request.abort(signal.reason);
    return;
  }
  function listener() {
    cleanup();
    request.abort(signal.reason);
  }
  function cleanup() {
    request.detachAbortSignal = null;
    signal.removeEventListener('abort', listener);
  }
  request.detachAbortSignal = cleanup;
  signal.addEventListener('abort', listener);
}
```

- Defer expensive derived work:
```js
const deferredText = useDeferredValue(searchText);
const searchResults = useMemo(
  () => computeMatches(deferredText),
  [deferredText],
);
```

If you follow these, your concurrency changes are less likely to introduce: UI stalls, racey shared state corruption, or resource leaks from lingering async listeners.