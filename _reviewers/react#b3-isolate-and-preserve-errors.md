---
title: Isolate and preserve errors
description: 'When executing callbacks and error paths, make failures deterministic
  and non-destructive:


  - Don’t silence errors in tests (assert what fails; remove mocks that hide failures).'
repository: facebook/react#b3
label: Error Handling
language: JavaScript
comments_count: 6
repository_stars: 251883
---

When executing callbacks and error paths, make failures deterministic and non-destructive:

- Don’t silence errors in tests (assert what fails; remove mocks that hide failures).
- Never change runtime semantics by environment (e.g., avoid `throw` only in `__DEV__`; use logging/`console.error` for diagnostics).
- If you call user/external code during rendering/flush/event phases, wrap each callback so one throw doesn’t prevent other necessary work; keep error propagation consistent.
- Ensure cleanup happens even if callback invocation throws (e.g., `try/finally` around callback maps/state).
- Preserve the “reason” for abort/closed signals—later errors should not overwrite the original abort/cleanup intent. If you create internal reasons, use stack-safe construction when a stack would be misleading or forbidden.

Example pattern (callback isolation + cleanup):

```js
const callbacks = new Map();

function handleResponse(msg) {
  if (msg.source !== '...-response') return;
  const {requestId, response} = msg;
  const cb = callbacks.get(requestId);
  if (!cb) return;
  callbacks.delete(requestId);
  try {
    cb(response);
  } finally {
    // If you chose not to delete earlier, do it here instead.
    callbacks.delete(requestId);
  }
}

function flushAndNotify(events) {
  for (let i = 0; i < events.length; i++) {
    try {
      events[i](); // user code
    } catch (e) {
      // report/propagate consistently; continue if required by invariants
    }
  }
}
```

Apply this standard anywhere React (or tooling) invokes user code, external runtimes, or relies on abort/closed coherence—ensuring both robustness and predictable error behavior.