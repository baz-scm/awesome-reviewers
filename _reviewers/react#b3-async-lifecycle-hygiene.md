---
title: Async lifecycle hygiene
description: 'Ensure concurrency code manages lifecycles explicitly: attach async
  work only with a clear shutdown path, detach listeners once the operation is terminal,
  and avoid keeping objects/promises alive past their usefulness. For UI/concurrent
  rendering, keep input updates synchronous but defer expensive derived computations
  to lower-priority work. Finally, use...'
repository: facebook/react#b3
label: Concurrency
language: JavaScript
comments_count: 5
repository_stars: 251883
---

Ensure concurrency code manages lifecycles explicitly: attach async work only with a clear shutdown path, detach listeners once the operation is terminal, and avoid keeping objects/promises alive past their usefulness. For UI/concurrent rendering, keep input updates synchronous but defer expensive derived computations to lower-priority work. Finally, use the correct scheduling primitive (microtask vs sync fallback) rather than behavior that only “works by accident”.

Guidelines:
- Listener cleanup: if you add event listeners to an AbortSignal (or similar), remove them when the request/operation reaches a terminal state to prevent retention.
- Promise hygiene: don’t create never-resolved promises as placeholders—use `Promise.resolve()` (or resolve/reject appropriately).
- Priority/deferred work: expensive derived computations (like tree walks/search) should be deferred so they don’t block higher-priority updates.
- Scheduling semantics: prefer the platform’s intended primitive (e.g., `queueMicrotask`/`scheduleMicrotask`) and don’t replace it with sync behavior unless you can prove it’s safe.

Example:
```js
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

// In React: keep controlled input sync, defer expensive derived work
const deferredSearchText = useDeferredValue(searchText);
const searchResults = useMemo(() => computeMatches(deferredSearchText), [deferredSearchText]);

// Avoid never-resolving promises
const p = Promise.resolve();
```