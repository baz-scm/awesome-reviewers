---
title: Manage async lifetimes
description: 'When code uses async control flow (streams, signals, deferred scheduling,
  or wake/pass pipelines), make the work’s lifetime explicit and safe.


  - **Bound and clean up:** If you attach listeners (e.g., `signal.addEventListener(''abort'',
  ...)`) or create long-lived async resources, ensure they are removed/detached when
  the operation reaches a terminal outcome....'
repository: facebook/react#b2
label: Concurrency
language: JavaScript
comments_count: 4
repository_stars: 251882
---

When code uses async control flow (streams, signals, deferred scheduling, or wake/pass pipelines), make the work’s lifetime explicit and safe.

- **Bound and clean up:** If you attach listeners (e.g., `signal.addEventListener('abort', ...)`) or create long-lived async resources, ensure they are removed/detached when the operation reaches a terminal outcome. Don’t let listeners keep large objects reachable indefinitely.
- **Avoid never-resolving promises:** If an async API is only a stub or unused path, return an already-resolved promise instead of one that never settles.
- **Don’t block urgent updates:** Keep high-priority UI updates synchronous (e.g., controlled input), but defer expensive derived computations so they can’t stall the update that changes the input.
- **Don’t rely on a single downstream async pass:** If a later phase (like `wakeChunk`) might not run depending on async conditions, move required state/debug updates to the initialization path so they happen deterministically.

Example (abort listener cleanup + no listener leaks):
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

Example (defer expensive derived work):
```js
const [searchTextState, setSearchTextState] = useState('');
const searchText = useDeferredValue(searchTextState);
const searchResults = useMemo(() => computeMatches(searchText), [searchText]);

function onInputChange(text) {
  // synchronous: keep the input responsive
  setSearchTextState(text);
}
```