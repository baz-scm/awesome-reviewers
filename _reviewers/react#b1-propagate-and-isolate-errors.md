---
title: Propagate and Isolate Errors
description: 'When handling failures, do three things consistently: (1) don’t silence
  or weaken errors (especially in tests/scripts/devtools), (2) make abort/fatal paths
  terminal so later success signaling can’t overwrite them, and (3) isolate any user/external
  callback so one throw doesn’t break cleanup or subsequent phases.'
repository: facebook/react#b1
label: Error Handling
language: JavaScript
comments_count: 8
repository_stars: 251878
---

When handling failures, do three things consistently: (1) don’t silence or weaken errors (especially in tests/scripts/devtools), (2) make abort/fatal paths terminal so later success signaling can’t overwrite them, and (3) isolate any user/external callback so one throw doesn’t break cleanup or subsequent phases.

Practical rules:
- Never intentionally suppress failures in tests; assert the specific failure signal/reason.
- Avoid DEV-only behavior that changes error semantics (e.g., don’t throw only in `__DEV__`).
- For fatal/aborted flows, prevent later “success” callbacks from running (e.g., set `onAllReady = noop`).
- Guard state transitions after abort/error so later chunks/events aren’t processed as if they were still valid (e.g., skip `triggerErrorOnChunk` when the chunk is already `ERRORED`).
- When calling user code (or code reachable from user-land), wrap each callback in its own `try/catch` so other queued work/cleanup still happens.
- Use error “shapes” deliberately: if stack capture is impossible/unhelpful, use stack-less reasons, but only if the downstream consumer already supports that representation.

Example pattern (per-callback isolation):
```js
function flushCallbacks(callbacks) {
  for (let i = 0; i < callbacks.length; i++) {
    try {
      callbacks[i]();
    } catch (e) {
      // report/record error, but do not prevent cleanup of remaining phases
      handleCallbackError(e);
    }
  }
}
```

Apply this standard to keep error propagation reliable, avoid DEV-only discrepancies, and ensure aborted/fatal renders don’t get accidentally “continued” or overwritten.