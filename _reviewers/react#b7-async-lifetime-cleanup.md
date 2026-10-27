---
title: Async lifetime cleanup
description: 'Ensure every async/concurrent side effect has a clear lifetime: if you
  attach listeners, schedule callbacks, or create promises, you must (1) detach/stop
  work when the operation reaches a terminal state, and (2) avoid retaining large
  objects or contexts longer than necessary. When execution can suspend and later
  resume, preserve third-party async context...'
repository: facebook/react#b7
label: Concurrency
language: JavaScript
comments_count: 5
repository_stars: 251888
---

Ensure every async/concurrent side effect has a clear lifetime: if you attach listeners, schedule callbacks, or create promises, you must (1) detach/stop work when the operation reaches a terminal state, and (2) avoid retaining large objects or contexts longer than necessary. When execution can suspend and later resume, preserve third-party async context explicitly (e.g., AsyncLocalStorage snapshot/restore).

Practical rules:
- Abort/listener cleanup: detach the abort listener on completion/terminal state so the listener doesn’t keep the Request (or other large graph) reachable for as long as the caller’s signal lives.
- Never-resolving promises: don’t create promises that never settle unless they’re actually awaited; use already-resolved promises when the result is irrelevant.
- Scheduling correctness: when using “microtask-like” utilities in different environments, implement a consistent next-tick/microtask strategy and ensure errors surface.
- Suspension/resumption context: use snapshot/restore for async context carriers so values remain correct after suspend.

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

Example (AsyncLocalStorage across suspend/resume):
```js
const store = new AsyncLocalStorage();
const snap = store.snapshot();
// before throwing/suspending: capture snapshot
// after resuming: restore snapshot around the resumed render work
snap.run(() => {
  // render after suspense with the same async context
});
```