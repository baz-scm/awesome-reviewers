---
title: Race-Safe Async Propagation
description: In concurrent/async code, never rely solely on static types or single-pass
  assumptions. Treat state as mutable, ensure event/listener lifecycle is explicit,
  avoid recursion in notification/wake paths, and defer expensive derived work so
  updates aren’t blocked.
repository: facebook/react#b13
label: Concurrency
language: JavaScript
comments_count: 4
repository_stars: 251893
---

In concurrent/async code, never rely solely on static types or single-pass assumptions. Treat state as mutable, ensure event/listener lifecycle is explicit, avoid recursion in notification/wake paths, and defer expensive derived work so updates aren’t blocked.

Apply these rules:

1) Re-check state at runtime (race/mutation safety)
- Even if a value is “typed” a certain way, it may have been mutated by other resolution/cleanup paths.
- Pattern: guard against terminal transitions (e.g., status/errored/null) right before acting.

2) Ensure async listener cleanup (lifecycle safety)
- For abort/cancel/signals, attach listeners only with a guaranteed detach path.
- Pattern: the listener should remove itself as soon as it fires (or when the owner reaches a terminal state).

3) Avoid recursion in hot async wake/notify loops
- If wake/initialize can trigger many dependents, recursive calls can stack overflow.
- Pattern: prefer iterative/local decision logic: check current status and call wake/reject directly.

4) Defer expensive derived work (responsiveness)
- Keep user input updates synchronous, but compute heavy derived results at lower priority (e.g., derived data via deferred values).

Concrete sketch:

```js
function initializeIfUnblocked(response, handler) {
  // Types may say BlockedChunk, but runtime mutation can change it.
  if (handler.deps !== 0 || handler.errored) return;
  const chunk = handler.chunk;
  if (chunk == null || chunk.status !== 'BLOCKED') return;

  // ... initialize chunk here (then notify waiters)
}

function attachAbortSignal(request, signal) {
  if (signal.aborted) {
    abort(request, signal.reason);
    return;
  }

  function listener() {
    // Detach first to avoid retaining request via the signal.
    signal.removeEventListener('abort', listener);
    abort(request, signal.reason);
  }

  signal.addEventListener('abort', listener);
}

function wakeChunkSafely(response, resolveListeners, value, initializedChunk) {
  // Avoid recursion when many listeners exist.
  // Decide what to do based on current status, then notify.
  // (Pseudo-logic)
  if (initializedChunk.status === 'INITIALIZED') {
    wakeChunk(response, resolveListeners, value, initializedChunk);
  } else if (initializedChunk.status === 'ERRORED') {
    rejectChunk(response, resolveListeners, initializedChunk.reason);
  }
}

// In UI code: keep input sync; defer derived computation.
// const deferredQuery = useDeferredValue(searchText);
// const results = useMemo(() => compute(deferredQuery), [deferredQuery]);
```

If you adopt this, concurrency bugs (racey state, leaks from listeners, and stack overflows in fan-out wake paths) become much less likely, and UI/UX remains responsive under load.