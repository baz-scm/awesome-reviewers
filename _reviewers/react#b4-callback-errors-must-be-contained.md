---
title: Callback errors must be contained
description: 'When your code invokes callback-like work (user event handlers, devtools
  inspection functions, runtime instruction handlers, etc.), treat it as potentially
  throwing: isolate failures per invocation, propagate them through the appropriate
  recovery/error channel, and never let a later failure overwrite a previously-authoritative
  abort/fatal reason.'
repository: facebook/react#b4
label: Error Handling
language: JavaScript
comments_count: 6
repository_stars: 251885
---

When your code invokes callback-like work (user event handlers, devtools inspection functions, runtime instruction handlers, etc.), treat it as potentially throwing: isolate failures per invocation, propagate them through the appropriate recovery/error channel, and never let a later failure overwrite a previously-authoritative abort/fatal reason.

Practical rules:
- Wrap each callback invocation in try/catch (or equivalent) so one callback failure doesn’t prevent required flushing/cleanup of other phases.
- Do not silence errors in tests or tooling; either assert on the error reason or return/emit a structured error (optionally with a cause).
- If the system is already aborted/fatal, ignore subsequent downstream errors so the original abort/failure reason remains coherent.
- For internal abort signals, use a consistent error “shape” (e.g., stack-free) and document the rationale; ensure consuming paths can handle that shape.
- Always clean up state/registrations (e.g., callback maps, pending markers) even if handling code throws (use try/finally around response/dispatch paths).

Example pattern:
```js
function runCallbackSafely(cb, payload, {onError, isAbortedRef}) {
  if (isAbortedRef.current) return; // preserve original abort reason
  try {
    return cb(payload);
  } catch (e) {
    // report but don't break other required work
    onError(e);
  }
}

// When handling multiple callbacks/phases:
for (const cb of callbacks) {
  runCallbackSafely(cb, arg, {onError: reportRecoverableError, isAbortedRef});
}
```

Apply this especially around:
- user-facing event phases (e.g., transition/view lifecycle hooks)
- devtools/runtime instruction handling
- any async/streaming flow where abort/fatal state can occur and must remain stable.