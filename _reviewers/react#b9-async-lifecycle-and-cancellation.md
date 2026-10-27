---
title: Async lifecycle and cancellation
description: 'When adding async/concurrent behavior, treat it as a managed lifetime:
  ensure cancellation/cleanup is correct, scheduling is realistic, and work doesn’t
  block higher-priority updates.'
repository: facebook/react#b9
label: Concurrency
language: JavaScript
comments_count: 6
repository_stars: 251891
---

When adding async/concurrent behavior, treat it as a managed lifetime: ensure cancellation/cleanup is correct, scheduling is realistic, and work doesn’t block higher-priority updates.

Apply these rules:
- **Detach cancellation listeners on terminal completion.** If you attach `abort`/timeout listeners, remove them once the async operation can no longer change state to avoid retaining references.
- **Avoid never-resolving Promises.** They can keep resources and dependent logic alive indefinitely; use `Promise.resolve()` (or ensure the Promise is resolved/rejected).
- **Use correct microtask scheduling (or safe fallbacks).** Prefer real `queueMicrotask`/`Promise`-based microtasks; if you must fallback, implement it in a way that doesn’t change observable ordering unexpectedly.
- **Defer heavy derived computation.** Keep controlled input updates synchronous, but run expensive “search/match/walk” work at deferred/transition priority so typing/interaction stays responsive.

Example (abort listener cleanup pattern):
```js
export function attachAbortSignal(request, signal) {
  if (signal.aborted) {
    abort(request, signal.reason);
    return;
  }

  function listener() {
    request.detachAbortSignal?.(); // detach first to avoid retention
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

If you also depend on async context (e.g., third-party AsyncLocalStorage), capture/restore it explicitly across suspend/resume rather than assuming it will propagate automatically across promise boundaries.