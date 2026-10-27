---
title: Defensive error propagation
description: 'When code runs across async boundaries (render phases, callbacks, streaming/flight),
  make error handling *causal, non-silent, and isolated*:


  - **Preserve the authoritative failure/abort reason.** Once a request/stream is
  aborted or closed, do not allow later downstream errors to replace the original
  abort reason.'
repository: facebook/react#b7
label: Error Handling
language: JavaScript
comments_count: 7
repository_stars: 251888
---

When code runs across async boundaries (render phases, callbacks, streaming/flight), make error handling *causal, non-silent, and isolated*:

- **Preserve the authoritative failure/abort reason.** Once a request/stream is aborted or closed, do not allow later downstream errors to replace the original abort reason.
- **Isolate user/instruction callbacks.** If React calls user-provided hooks/events (or processes host/external runtime instructions), wrap each callback in a local try/catch so one failure doesn’t prevent other phases from running or other errors from being reported.
- **Never rely on `__DEV__`-only throwing.** If something should never happen, report/log consistently; avoid conditional throw behavior that changes correctness only in dev.
- **Use stack-safe internal control signals.** For internal “abort for cleanup” reasons, avoid capturing stacks (or explicitly justify/limit it) to prevent leaks. If the consumer path already supports non-Error values, a string reason can be acceptable.
- **Tests must assert real failures and restore mutated globals.** Don’t silence errors; if you temporarily change globals like `Error.stackTraceLimit`, always restore them.

Example patterns:

```js
// 1) Preserve abort reason
function reportGlobalError(weakResponse, error) {
  const response = unwrapWeakResponse(weakResponse);
  if (response._closed) return; // don’t overwrite abort/close cause
  // ...propagate error chunk
}

// 2) Isolate user callbacks
for (const evt of pendingEvents) {
  try {
    evt(pendingTypes);
  } catch (e) {
    // route/report without breaking other flush/error handling
    // (e.g., trigger recoverable error path)
  }
}

// 3) Stack-safe internal abort reason
const abortReason = createErrorWithoutStack(
  'This render completed successfully. Aborting cacheSignals for cleanup.'
);
request.cacheController.abort(abortReason);

// 4) No __DEV__-conditional throw
if (__DEV__) {
  // validate + throw/log consistently in the same way as prod, or just log.
}
```

Applying this standard reduces flaky tests, prevents misleading error causality, avoids stack leaks from control-flow signals, and ensures one callback failure doesn’t destabilize the rest of the system’s error recovery/flush behavior.