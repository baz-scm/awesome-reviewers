---
title: Preserve Concurrency Semantics
description: When code runs with concurrent rendering or async scheduling, you must
  preserve the intended scheduling/priority semantics, keep user-facing updates responsive,
  and avoid retaining work via long-lived listeners.
repository: facebook/react#b17
label: Concurrency
language: JavaScript
comments_count: 6
repository_stars: 251891
---

When code runs with concurrent rendering or async scheduling, you must preserve the intended scheduling/priority semantics, keep user-facing updates responsive, and avoid retaining work via long-lived listeners.

Apply these rules:
1) Preserve scheduling eligibility (lanes/priorities)
- If a path uses eager results or speculative comparisons, ensure the update’s priority/eligibility still matches the real commit/interrupt semantics.
- Don’t “normalize” scheduling fields (e.g., lane) in a way that changes when the update can be applied after an interrupt.

2) Defer expensive derived work
- Update controlled/interactive state synchronously.
- Compute derived results (e.g., searching/filtering a large tree) at transition/deferred priority so the input update is not blocked.

3) Clean up async listeners to avoid retention
- If you attach abort/event listeners to long-lived objects (e.g., Request, streams), detach them when the request reaches a terminal state.

4) Use correct scheduling primitives across environments
- Implement `scheduleMicrotask` with a feature check for `queueMicrotask` and a safe fallback.

Example patterns:
```js
// 2) Sync input, defer derived computation
function onChange(text) {
  setSearchTextState(text);           // sync
  // derived results computed via deferred/transition priority
  // e.g. const deferredText = useDeferredValue(searchText)
}

// 3) Abort listener cleanup
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

// 4) scheduleMicrotask with fallback
export const scheduleMicrotask =
  typeof queueMicrotask === 'function'
    ? queueMicrotask
    : cb => {
        Promise.resolve(null).then(cb).catch(err => {
          setTimeout(() => { throw err; });
        });
      };
```
