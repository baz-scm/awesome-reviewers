---
title: Async lifecycle correctness
description: 'When code crosses async boundaries (scheduling, streaming, events, suspension),
  write with an explicit lifecycle and ordering model:


  - Re-check mutable state at the point you act (static types may describe “what it
  was”, not “what it is now”). If in-place mutation can happen before the final step,
  keep runtime guards/status checks.'
repository: facebook/react#b8
label: Concurrency
language: JavaScript
comments_count: 7
repository_stars: 251889
---

When code crosses async boundaries (scheduling, streaming, events, suspension), write with an explicit lifecycle and ordering model:

- Re-check mutable state at the point you act (static types may describe “what it was”, not “what it is now”). If in-place mutation can happen before the final step, keep runtime guards/status checks.
- Attach abort/cleanup work only for the needed window, and detach immediately on terminal completion/abort to avoid retaining request/signal/closures.
- Be intentional about scheduling priority: keep urgent updates synchronous, defer expensive derived work, and standardize microtask scheduling via a shared helper (including correct fallback/error handling).
- When multiple outputs must not be split by backpressure/order constraints, represent and flush them as a single atomic unit.

Example (pattern for listener lifecycle):

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

Example (pattern for correct scheduling abstraction):

```js
export const scheduleMicrotask =
  typeof queueMicrotask === 'function'
    ? queueMicrotask
    : cb => {
        Promise.resolve(null).then(cb).catch(err => {
          setTimeout(() => { throw err; });
        });
      };
```

If you can’t state the lifecycle/priority/atomicity guarantees in a comment near the code, reviewers should request changes until you can.