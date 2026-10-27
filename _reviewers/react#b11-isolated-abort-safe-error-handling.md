---
title: Isolated, abort-safe error handling
description: 'When adding error handling in render/async pipelines, follow four rules:


  1) Never silence errors (and never make tests ignore them)

  - If something can fail, ensure the failure is surfaced to the caller/test (assert
  abort reason, or return an error payload instead of omitting data).'
repository: facebook/react#b11
label: Error Handling
language: JavaScript
comments_count: 10
repository_stars: 251894
---

When adding error handling in render/async pipelines, follow four rules:

1) Never silence errors (and never make tests ignore them)
- If something can fail, ensure the failure is surfaced to the caller/test (assert abort reason, or return an error payload instead of omitting data).

2) Preserve abort/close provenance
- After a request is aborted/closed, do not allow later downstream errors to replace the original abort reason.
- Guard error propagation paths so errored/closed state can’t trigger “wrong-shaped” error handling.

3) Isolate user-code callback failures
- Any code path that invokes user/host callbacks (e.g., view transition event handlers, external runtime instruction functions) should catch exceptions per-callback so one failure doesn’t break phase flushing, recovery, or remaining work.

4) Use intentional error shapes and avoid dev-only throwing
- Create errors appropriate to the channel: internal cleanup signals should not capture stacks (e.g., “without stack” errors).
- Don’t conditionally throw based on __DEV__; if dev-only diagnostics are needed, use logging or non-throwing behavior.

Example patterns:

- Abort-safe propagation guard:
```js
function reportGlobalError(weakResponse, error) {
  const response = unwrapWeakResponse(weakResponse);
  if (response._closed) return; // don’t overwrite abort reason
  // ... propagate original abort/errored state
}
```

- Isolate callback errors:
```js
for (let i = 0; i < pendingEvents.length; i++) {
  try {
    pendingEvents[i](pendingTypes);
  } catch (e) {
    // Route to the existing error mechanism; keep the pipeline coherent.
    onRecoverableError?.(e);
  }
}
```

- Internal cleanup abort without stack:
```js
const abortReason = createErrorWithoutStack(
  'Render completed successfully; aborting cacheSignals for cleanup.',
);
request.cacheController.abort(abortReason);
```

Applying this keeps errors actionable, prevents incorrect “successful render” signaling, maintains consistent abort semantics, and ensures rendering/recovery isn’t derailed by user callback exceptions or dev-only throwing behavior.