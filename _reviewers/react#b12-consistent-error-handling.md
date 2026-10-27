---
title: Consistent error handling
description: 'Treat errors/abort reasons as first-class, deterministic outcomes.


  Rules:

  1) Never silence or hide failures in tests or user-visible paths—assert/report the
  actual error/abort reason.'
repository: facebook/react#b12
label: Error Handling
language: JavaScript
comments_count: 8
repository_stars: 251896
---

Treat errors/abort reasons as first-class, deterministic outcomes.

Rules:
1) Never silence or hide failures in tests or user-visible paths—assert/report the actual error/abort reason.
2) Never throw only in __DEV__/feature flags; behavior should be consistent across builds.
3) When calling user code or external handlers during “flush”/iteration, isolate failures: catch per-callback so one throw doesn’t break the remaining phase semantics or skip other cleanup/handlers.
4) Preserve error coherence: once you’ve recorded/claimed an abort reason, don’t overwrite it with later errors; if a reason must be a non-user internal signal, use a safe shape (e.g., stackless reason) so downstream doesn’t misinterpret it.
5) If returning structured data on failure (e.g., tool payloads), return an error object (optionally with the original cause), not “success-with-missing-fields.”

Example (isolating callback errors during flushing):
```js
function flushCallbacks(events) {
  for (let i = 0; i < events.length; i++) {
    const cb = events[i];
    try {
      cb();
    } catch (e) {
      // Report/propagate without preventing later callbacks/cleanup.
      reportRecoverableError(e);
    }
  }
}
```

Example (abort reason coherence):
```js
let claimed = false;
function reportGlobalError(reason) {
  if (claimed) return;        // don’t replace an existing abort reason
  if (aborted) { claimed = true; setAbortReason(reason); }
}
```