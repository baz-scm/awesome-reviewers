---
title: Reliable error propagation
description: 'Use production-grade error handling that (1) never hides failures, (2)
  isolates user-code failures, and (3) preserves the correct failure outcome.


  Checklist:'
repository: facebook/react#b2
label: Error Handling
language: JavaScript
comments_count: 6
repository_stars: 251882
---

Use production-grade error handling that (1) never hides failures, (2) isolates user-code failures, and (3) preserves the correct failure outcome.

Checklist:
1) Don’t silence errors in tests. Assert the error/abort reason explicitly.
2) Never make critical error behavior dev-only. If an error must throw/propagate, it must be reachable in production too.
3) When React (or your system) invokes user-provided callbacks during a multi-phase flush, wrap each callback so one failure doesn’t prevent remaining callbacks/cleanup from running.
4) Don’t `throw` conditionally on `__DEV__`. If dev-only diagnostics are needed, use logging/`console.error` instead.
5) For internal abort/cleanup signals, use an error/reason shape appropriate for the channel (e.g., omit stack when it’s not useful/desired) and don’t let later downstream errors overwrite the original abort reason.
6) After fatal failure, prevent “success” callbacks from running later.

Example (per-callback isolation during flush):
```js
for (let i = 0; i < pendingEvents.length; i++) {
  try {
    pendingEvents[i](pendingTypes);
  } catch (err) {
    // Handle/report without preventing remaining phases/cleanup.
    // (e.g., call onRecoverableError, record, or schedule recovery)
  }
}
```
Example (test assertion, not silencing):
```js
serverAct(() => {
  prerender(<App />, {
    signal,
    onError(errors) {
      expect(String(errors[0])).toContain('aborted');
    },
  });
});
```