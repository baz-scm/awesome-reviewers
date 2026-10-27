---
title: Async lifetime and state
description: 'In concurrent/async code, assume runtime state can differ from static
  types (objects are mutated and transitions can be interleaved). Therefore:


  - **Guard real state transitions at runtime** (don’t rely on type-only guarantees
  when objects mutate in place).'
repository: facebook/react#b12
label: Concurrency
language: JavaScript
comments_count: 7
repository_stars: 251896
---

In concurrent/async code, assume runtime state can differ from static types (objects are mutated and transitions can be interleaved). Therefore:

- **Guard real state transitions at runtime** (don’t rely on type-only guarantees when objects mutate in place).
- **Deterministically clean up async resources** (detach listeners, release references) once you hit a terminal/finished state—otherwise you can leak requests/signals/promises.
- **Use a consistent scheduling abstraction across environments** (feature-test microtask APIs; don’t silently replace them with synchronous execution that changes ordering).
- **Ensure every initialization path triggers the same wake/propagation behavior** (missing it in one branch can stall the whole system).

Example (abort listener cleanup):
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

Example (scheduling abstraction):
```js
export const scheduleMicrotask =
  typeof queueMicrotask === 'function'
    ? queueMicrotask
    : cb => {
        Promise.resolve().then(cb);
      };
```

Apply these rules to any code that suspends, drains queues, mutates shared state, or coordinates lifetimes across callbacks/promises/signals.