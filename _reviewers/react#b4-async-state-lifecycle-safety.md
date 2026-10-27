---
title: Async state lifecycle safety
description: 'When implementing async/concurrency logic, assume the “current” state
  you captured may be invalid later because objects are mutated by other async paths.
  Treat lifecycle/ordering as part of correctness:'
repository: facebook/react#b4
label: Concurrency
language: JavaScript
comments_count: 6
repository_stars: 251885
---

When implementing async/concurrency logic, assume the “current” state you captured may be invalid later because objects are mutated by other async paths. Treat lifecycle/ordering as part of correctness:

- **Guard runtime state transitions, not just static types.** If an object is mutated in place (e.g., graph nodes/chunks), perform explicit runtime checks for terminal/error/status before acting.
- **Ensure every path performs required side-effects.** If initialization can occur without reaching the usual “wake/propagate” path, move or duplicate the necessary bookkeeping so it runs consistently.
- **Deterministically clean up async listeners/timers.** If you attach an abort/event listener, detach it once the target reaches a terminal status to avoid retaining large objects until the caller’s signal completes.
- **Use a scheduling abstraction that matches the runtime’s microtask/task semantics, with safe fallbacks.** Prefer `queueMicrotask` when available; otherwise use a Promise-based fallback that still runs asynchronously and doesn’t assume Promise globals are missing.
- **Avoid re-entrancy bugs from shared mutable globals.** If rendering can nest/sync-reenter, any shared temp used by replacers/formatters must be saved/restored.

Example (detach abort listener):
```js
export function attachAbortSignal(request, signal) {
  if (signal.aborted) {
    abort(request, signal.reason);
    return;
  }
  function detach() {
    request.detachAbortSignal = null;
    signal.removeEventListener('abort', listener);
  }
  function listener() {
    detach();
    abort(request, signal.reason);
  }
  request.detachAbortSignal = detach;
  signal.addEventListener('abort', listener);
}
```

Example (microtask scheduling with fallback):
```js
function handleErrorInNextTick(error) {
  setTimeout(() => { throw error; });
}
export const scheduleMicrotask =
  typeof queueMicrotask === 'function'
    ? queueMicrotask
    : cb => {
        Promise.resolve(null).then(cb).catch(handleErrorInNextTick);
      };
```

Apply this checklist to any concurrency code: graph-node initialization, abort/cancellation handling, and scheduling abstractions—if a missing cleanup or missing propagation can occur on one path, treat it as a correctness bug, not a refactor.”}]}