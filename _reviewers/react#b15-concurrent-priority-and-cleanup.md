---
title: Concurrent priority and cleanup
description: When your code runs under concurrency (interruptible renders, async streaming,
  or UI concurrent updates), treat **priority/lane correctness** and **async lifetime
  cleanup** as mandatory.
repository: facebook/react#b15
label: Concurrency
language: JavaScript
comments_count: 5
repository_stars: 251891
---

When your code runs under concurrency (interruptible renders, async streaming, or UI concurrent updates), treat **priority/lane correctness** and **async lifetime cleanup** as mandatory.

**Rules**
1. **Never treat speculative state as committed.** If an “eager bailout”/cached result is derived from unfinished work, ensure the update’s scheduling metadata (e.g., React’s lane/priority) is set so interrupting renders either (a) apply immediately when correct or (b) defer when urgent output would otherwise be wrong.
2. **Keep urgent updates unblocked; defer expensive/derived work.** For controlled inputs, update synchronously. Compute derived results (e.g., searching, filtering, tree walks) at lower priority using deferred/transition-priority mechanisms.
3. **Attach abort/cleanup handlers, then detach on terminal completion.** If you add an `abort` event listener or similar, remove it when the async operation reaches a terminal state; otherwise you can accidentally retain requests/signals for the lifetime of the caller’s signal.
4. **Use the right scheduling primitive per environment** (microtask vs fallback) and ensure failures surface (don’t silently swallow errors in scheduling fallbacks).

**Example patterns**
- *Defer derived computation while keeping input sync:*
  ```js
  function onSearchChange(text) {
    setSearchTextState(text); // sync input
    // derived computation happens via deferred/dependency-driven state elsewhere
  }
  ```
- *Detach abort listeners on completion:*
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

If a change touches interruption/priority, derived computation, or abort/stream lifetime, require reviewers to explicitly check these three aspects: **(a) priority/lane correctness**, **(b) responsiveness (no blocking urgent updates)**, and **(c) cleanup (listeners removed on terminal state).**