---
title: Isolate and Preserve Errors
description: 'When executing callbacks/handlers or transitioning error/abort states,
  treat errors as first-class outcomes: isolate failures, preserve the original failure
  reason, and don’t hide errors behind DEV-only behavior.'
repository: facebook/react#b17
label: Error Handling
language: JavaScript
comments_count: 10
repository_stars: 251891
---

When executing callbacks/handlers or transitioning error/abort states, treat errors as first-class outcomes: isolate failures, preserve the original failure reason, and don’t hide errors behind DEV-only behavior.

**Rules**
1. **Isolate user code**: if a phase calls user/event callbacks (e.g., transition/event handlers, instruction functions), wrap each callback so one failure doesn’t break the rest of the flushing/processing pipeline.
2. **Preserve abort/fatal coherence**: once you’ve decided the render/task is aborted/closed or has hit a fatal error, prevent later errors from overwriting the abort reason and prevent later “success” signaling.
3. **Use the right error shape**: internal cleanup reasons can intentionally omit stack; if you use non-`Error` values (e.g., strings), ensure every consumer path already supports that shape.
4. **Never silence in tests/tools**: don’t swallow errors in tests; assert on the specific reason/state.
5. **Avoid conditional throwing**: don’t `throw` only under `__DEV__`; prefer consistent runtime behavior (or report/log) across builds.

**Example (per-callback isolation + abort guard)**
```js
function flushViewTransitionEvents(pendingEvents, isClosed, onError) {
  if (isClosed) return;
  for (let i = 0; i < pendingEvents.length; i++) {
    const cb = pendingEvents[i];
    try {
      cb();
    } catch (err) {
      onError(err); // handle/report, but continue flushing remaining callbacks
    }
  }
}
```

Applying these keeps error behavior predictable, prevents incomplete work after a single handler throws, and ensures the final reported outcome matches the system’s actual terminal state.