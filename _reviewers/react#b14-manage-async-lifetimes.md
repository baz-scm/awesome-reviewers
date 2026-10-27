---
title: Manage async lifetimes
description: 'When adding async work (streams, abort handlers, suspense/resume, microtasks,
  deferred computations), make lifetimes and scheduling explicit: ensure cleanup on
  all terminal/cancel paths, avoid blocking critical synchronous updates, preserve
  async context across suspension, and don’t rely on incidental `.then()` side effects.'
repository: facebook/react#b14
label: Concurrency
language: JavaScript
comments_count: 6
repository_stars: 251893
---

When adding async work (streams, abort handlers, suspense/resume, microtasks, deferred computations), make lifetimes and scheduling explicit: ensure cleanup on all terminal/cancel paths, avoid blocking critical synchronous updates, preserve async context across suspension, and don’t rely on incidental `.then()` side effects.

Action checklist:
- **Attach + detach**: Any event listener or callback registered to a long-lived signal must be removed when the async operation reaches a terminal state; otherwise you’ll retain unrelated objects.
- **Never leave async resources pending**: Avoid creating never-resolving promises just to satisfy an interface—use a resolved value when you’re stubbing.
- **Defer expensive derived work**: Keep controlled/UI-critical state updates synchronous, but compute heavy derived data (search, tree walks) at transition/deferred priority so input remains responsive.
- **Preserve async context across suspend/resume**: If third-party async context exists (e.g., `AsyncLocalStorage`), capture/restore it when the render suspends and later resumes.
- **Make scheduling semantics deterministic**: Use a correct `scheduleMicrotask` implementation (and safe fallback) and ensure critical logic doesn’t accidentally depend on whether some code path adds a `.then()`.

Example (abort listener cleanup + no retention):
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

Example (defer expensive search while keeping input sync):
```js
const [text, setText] = useState('');
const deferredText = useDeferredValue(text);
const results = useMemo(() => computeMatches(deferredText), [deferredText]);
// setText on input change stays synchronous; computeMatches runs at lower priority.
```

Example (microtask scheduling with deterministic fallback):
```js
const scheduleMicrotask =
  typeof queueMicrotask === 'function'
    ? queueMicrotask
    : cb => Promise.resolve(null).then(cb);
```