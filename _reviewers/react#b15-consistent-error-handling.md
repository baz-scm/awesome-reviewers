---
title: Consistent Error Handling
description: 'Coding standard for error handling and failure scenarios:


  1) Never silence real failures

  - Tests should assert on the observable failure (e.g., abort reason) rather than
  swallowing errors.'
repository: facebook/react#b15
label: Error Handling
language: JavaScript
comments_count: 8
repository_stars: 251891
---

Coding standard for error handling and failure scenarios:

1) Never silence real failures
- Tests should assert on the observable failure (e.g., abort reason) rather than swallowing errors.
- Keep intentional throws in production code unless there is a deliberate, documented fallback.

2) Make behavior consistent in dev and prod
- Do not “throw only in __DEV__”. If it’s an error condition, handle it consistently everywhere (or log instead of throwing when failure is expected/optional).

3) Isolate failures when calling user code
- If you invoke user callbacks/events, wrap each callback so one throw doesn’t break other required cleanup/phase handling.

4) Preserve abort/failure coherency
- After abort/cleanup begins, don’t let later downstream errors overwrite the original abort reason.
- Guard state transitions so you don’t re-trigger error paths assuming a chunk is in a compatible state (e.g., skip triggering error logic for already-errored chunks).
- For internal cleanup signals, prefer stackless error-like values when capturing a stack is unnecessary or unsafe.

Example (per-callback isolation):
```js
for (let i = 0; i < pendingEvents.length; i++) {
  const cb = pendingEvents[i];
  try {
    cb(pendingTypes);
  } catch (e) {
    // Ensure this callback's failure doesn't prevent required cleanup/other callbacks.
    // Route through the appropriate recoverable error mechanism.
    onRecoverableError(e);
  }
}
```

Example (preserve abort reason):
```js
export function reportGlobalError(weakResponse, error) {
  const response = unwrapWeakResponse(weakResponse);
  if (response._closed) return; // avoid replacing the abort/coherent terminal reason
  // otherwise propagate the error
}
```