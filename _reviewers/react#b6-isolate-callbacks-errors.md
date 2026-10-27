---
title: Isolate Callbacks Errors
description: When you invoke callbacks or event handlers (including built-ins that
  trigger userland code), treat them as failure-prone and keep the rest of the pipeline
  correct.
repository: facebook/react#b6
label: Error Handling
language: JavaScript
comments_count: 7
repository_stars: 251888
---

When you invoke callbacks or event handlers (including built-ins that trigger userland code), treat them as failure-prone and keep the rest of the pipeline correct.

**Rules**
1. **Wrap each callback invocation in `try/catch`** so one handler failure doesn’t skip later phases/work.
2. **Preserve the primary failure/abort reason**: once you’ve aborted/rejected for a cause, don’t let later, unrelated errors overwrite the coherent reason.
3. **Propagate errors explicitly**—don’t silently ignore failures in tests/tools/scripts. Assert or return an error payload.
4. **Use consistent error shapes**: prefer `Error` (optionally with `{cause}`) and document any deliberate exceptions (e.g., internal cleanup signals that must be stackless, or other downstream-compatible non-`Error` values).
5. **Avoid conditional throwing on environment flags** (`__DEV__`): behavior should be consistent; if you only want diagnostics, use logging instead of throwing.

**Example pattern**
```js
function flushViewTransitionEvents(pendingEvents) {
  if (pendingEvents == null) return;
  for (let i = 0; i < pendingEvents.length; i++) {
    const handler = pendingEvents[i];
    try {
      handler();
    } catch (error) {
      // Report via the system’s recoverable-error / error chunk path
      // (exact mechanism depends on the module)
      reportError(error);
      // continue flushing remaining handlers/phases
    }
  }
}
```

Apply this standard anywhere user code can run (event handlers, injected callbacks, hook inspection, external runtime instruction handlers) to ensure correctness and debuggability under failure.