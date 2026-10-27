---
title: async Boundary Safety
description: 'When code crosses async/streaming boundaries (suspense, hydration, streaming/flight,
  abort signals, deferred work), treat the boundary like a synchronization point:
  keep required state/context ordering around potential suspension, validate mutable
  state transitions at runtime (not just types), and clean up async lifetimes so nothing
  is retained past...'
repository: facebook/react#b5
label: Concurrency
language: JavaScript
comments_count: 5
repository_stars: 251886
---

When code crosses async/streaming boundaries (suspense, hydration, streaming/flight, abort signals, deferred work), treat the boundary like a synchronization point: keep required state/context ordering around potential suspension, validate mutable state transitions at runtime (not just types), and clean up async lifetimes so nothing is retained past completion.

Apply these rules:

1) Don’t move state/context pushes past operations that may suspend
- If a function you call can suspend/abort/stream, keep the related push/pop (context, host context, etc.) correctly paired in the surrounding enter/update flow so unwind logic can’t pop a value that was never pushed.

2) Guard against “type says X, runtime is Y” for mutated shared objects
- If an object can be mutated in place by other paths (e.g., drained cyclic references, error propagation), add explicit runtime checks before acting.

3) Always detach abort listeners / async handlers at terminal states
- If you attach an `abort` listener, remove it when the request reaches a terminal status; otherwise the listener (and retained Request/signal) can stay reachable indefinitely.

4) Choose the right priority for derived/expensive work
- Keep user-controlled input updates synchronous, but derive expensive results at deferred/transition priority so async scheduling doesn’t block the next input render.

5) Use a deterministic async primitive with a fallback
- Prefer `queueMicrotask` when present; otherwise provide a safe fallback.

Example pattern (abort cleanup):
```js
export function attachAbortSignal(request, signal) {
  if (signal.aborted) {
    abort(request, signal.reason);
    return;
  }
  function listener() {
    detach();
    abort(request, signal.reason);
  }
  function detach() {
    request.detachAbortSignal = null;
    signal.removeEventListener('abort', listener);
  }
  request.detachAbortSignal = detach;
  signal.addEventListener('abort', listener);
}
```

These practices prevent race/mismatch bugs that only appear under suspense/hydration/streaming timing, and they avoid memory/lifetime leaks from leftover async listeners.