---
title: Preserve concurrency invariants
description: In concurrent/async code, treat *priority, scheduling, and object lifetime*
  as correctness—not just performance. Ensure that interrupts, bailouts, and nested
  rendering can’t cause stale state, wrong priority, or leaked references.
repository: facebook/react#b16
label: Concurrency
language: JavaScript
comments_count: 7
repository_stars: 251891
---

In concurrent/async code, treat *priority, scheduling, and object lifetime* as correctness—not just performance. Ensure that interrupts, bailouts, and nested rendering can’t cause stale state, wrong priority, or leaked references.

Practical rules:
- **Preserve priority semantics (e.g., lanes) across eager bailouts.** If you adjust/clear a lane, confirm it still allows the right interrupting render to apply cached eager state without replaying from an incorrect base.
- **Restore/avoid destructive mutations that outlive their intended scope.** If a code path mutates task/request fields for diagnostics or replay, restore previous values before returning to logic that assumes stable identity.
- **Defer expensive derived computations; keep input/controlled updates synchronous.** Compute-heavy searches/derivations should run at transition priority so they can’t block user input.
- **Detach listeners at terminal states to prevent retention and races.** When using abort signals or other event listeners, remove the listener once the request reaches a terminal status.
- **Use a reliable microtask scheduler abstraction.** Prefer feature detection (e.g., `queueMicrotask`) with a safe fallback.

Example pattern (combines priority + cleanup + safe scheduling):
```js
function scheduleMicrotaskSafe(callback) {
  if (typeof queueMicrotask === 'function') return queueMicrotask(callback);
  Promise.resolve(null).then(callback).catch(err => { setTimeout(() => { throw err; }); });
}

function attachAbortSignal(request, signal) {
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

function handleSearchInput(text) {
  // keep input update sync
  setSearchTextState(text);
  // defer derived/tree-walk work
  const deferred = useDeferredValue(text);
  const results = useMemo(() => expensiveTreeWalk(deferred), [deferred]);
  return results;
}
```

Checklist for code review:
- Does any logic change lane/priority, and is it correct under interruption?
- Any destructive mutations/leaked globals that might persist past a replay/suspense boundary?
- Are any listeners retained past terminal state?
- Are expensive derived computations deferred to transition priority?
- Are async scheduling primitives (microtasks) implemented robustly for all target environments?