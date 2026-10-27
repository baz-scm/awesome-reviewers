---
title: Handle errors explicitly
description: 'When errors can occur (user callbacks, external runtime instructions,
  abort/fatal flows), do not silently ignore them or let them corrupt control-flow.
  Instead:'
repository: facebook/react#b13
label: Error Handling
language: JavaScript
comments_count: 10
repository_stars: 251893
---

When errors can occur (user callbacks, external runtime instructions, abort/fatal flows), do not silently ignore them or let them corrupt control-flow. Instead:

1) Isolate user/external callback failures
- Wrap each callback invocation in try/catch so one failing callback doesn’t prevent required cleanup or other callbacks from running.
- Use try/finally for bookkeeping (e.g., maps of pending callbacks) to avoid leaks if the callback throws.

```js
for (let i = 0; i < callbacks.length; i++) {
  try {
    callbacks[i]();
  } catch (e) {
    reportError(e); // propagate/log according to platform
  }
}

// message->callback example
try {
  callback(response);
} finally {
  evalRequestCallbacks.delete(requestId);
}
```

2) Keep abort/fatal state coherent
- After a fatal error, prevent later “success” signaling (e.g., set `onAllReady = noop`).
- Don’t overwrite an abort reason with downstream/later errors; guard error propagation based on chunk/task status.
- For internal-only abort reasons, use an error type/constructor that matches the contract (e.g., “no stack” cleanup reasons).

3) Don’t make error behavior build-dependent
- Avoid `throw` conditioned on `__DEV__`; keep throwing/handling semantics consistent across environments.

4) Never silence failures in tests/infra
- Tests should assert on the actual error/abort reason instead of passing with suppressed errors.
- Scripts/CI should fail the process when the underlying operation fails (non-zero exit), not just log to stdout.

If you apply these rules consistently, you’ll get predictable error propagation, correct abort/fatal semantics, and fewer “works in DEV but fails in prod” surprises.