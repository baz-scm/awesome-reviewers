---
title: Propagate and isolate errors
description: When code encounters failures—especially during rendering/event/inspection
  phases—do not silence them, do not hide them behind DEV-only logic, and isolate
  failures so one bad callback doesn’t break the rest.
repository: facebook/react#b8
label: Error Handling
language: JavaScript
comments_count: 12
repository_stars: 251889
---

When code encounters failures—especially during rendering/event/inspection phases—do not silence them, do not hide them behind DEV-only logic, and isolate failures so one bad callback doesn’t break the rest.

Practical rules:
1) Never silence errors in tests: capture them (e.g., via onError), assert the expected error/abort reason, and fail the test when unexpected errors occur.
2) Ensure failure detection/guards work in production: don’t gate essential error throwing/counters behind __DEV__ such that production can’t fail fast.
3) Avoid “throw only in __DEV__”: if you need diagnostics, use console.error/warnings in DEV instead of conditional throws.
4) When executing callbacks or doing phase work that can trigger user code, wrap each callback independently (try/catch) so remaining phases still flush/cleanup.
5) Preserve error shape and context: return/emit an Error (or an Error-like object) with the underlying cause when possible; if you intentionally use a non-Error reason, ensure all consumers already handle that shape and document why.

Example pattern (isolating callback errors):
```js
for (let i = 0; i < callbacks.length; i++) {
  const cb = callbacks[i];
  try {
    cb();
  } catch (err) {
    // Report via the framework’s recoverable mechanism instead of aborting the whole phase.
    onRecoverableError?.(err);
  }
}
```

Example pattern (tests shouldn’t silence):
```js
let errors = [];
await serverAct(() => {
  prerender(App, {
    onError: e => errors.push(e),
  });
});
expect(errors[0].message).toBe('This operation was aborted');
```