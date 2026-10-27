---
title: Robust Error Handling
description: 'Adopt a consistent error-handling pattern across async work, user callbacks,
  and tests.


  **Rules**

  1) **Don’t silence failures**: tests/CI should assert or propagate errors—never
  hide them.'
repository: facebook/react#b9
label: Error Handling
language: JavaScript
comments_count: 12
repository_stars: 251891
---

Adopt a consistent error-handling pattern across async work, user callbacks, and tests.

**Rules**
1) **Don’t silence failures**: tests/CI should assert or propagate errors—never hide them.
2) **No conditional throws on `__DEV__`**: if something must not throw, don’t throw only in dev; prefer `console.error`/error return paths.
3) **Isolate user code**: wrap user-supplied callbacks (event handlers, instruction handlers) in per-callback `try/catch` so one failure doesn’t break later phases.
4) **Preserve the primary failure/abort reason**: once a task/stream is aborted or closed, ignore later downstream errors so they can’t overwrite the abort reason.
5) **Always clean up**: restore global ambient state (e.g., `Error.stackTraceLimit`), close connections in all throw paths, and remove pending callback entries via `finally`.

**Example (user-callback isolation + cleanup)**
```js
function flushUserEvents(events) {
  if (!events) return;
  for (let i = 0; i < events.length; i++) {
    try {
      events[i](); // user code
    } catch (e) {
      // handle/report without breaking other callbacks
      onRecoverableError(e);
    }
  }
}

async function testThatRestoresAmbientSetting() {
  const prev = Error.stackTraceLimit;
  try {
    Error.stackTraceLimit = 50;
    await run();
  } finally {
    Error.stackTraceLimit = prev; // never leak global state
  }
}

function reportGlobalErrorIfNotClosed(response, error) {
  if (response._closed) return; // don’t replace abort reason
  report(error);
}
```

Apply this checklist when adding new built-ins, event/callback phases, streaming abort logic, devtools bridges, hydration/external instruction runtimes, or tests/CI scripts.