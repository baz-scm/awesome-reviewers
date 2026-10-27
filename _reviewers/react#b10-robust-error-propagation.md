---
title: Robust Error Propagation
description: When handling errors in async/render pipelines, ensure you (1) surface
  the correct error (don’t silence/overwrite cancellation reasons), (2) only propagate
  errors in the appropriate lifecycle state, and (3) isolate user/runtime callback
  failures so they don’t break subsequent phases.
repository: facebook/react#b10
label: Error Handling
language: JavaScript
comments_count: 6
repository_stars: 251894
---

When handling errors in async/render pipelines, ensure you (1) surface the correct error (don’t silence/overwrite cancellation reasons), (2) only propagate errors in the appropriate lifecycle state, and (3) isolate user/runtime callback failures so they don’t break subsequent phases.

Practical rules:
- **Don’t silence errors in tests**: assert the expected failure/abort reason rather than suppressing it.
- **Treat cancellation/abort reasons as immutable**: once a request/stream is closed or aborted, don’t replace that reason with later downstream errors.
- **Guard error propagation by state**: only trigger/route errors when the target chunk is in the right status; avoid treating errored/aborted chunks as other chunk types.
- **Wrap user callbacks**: if you call user-provided handlers/events, catch per-callback and avoid breaking the renderer’s phase sequencing.
- **Keep behavior consistent across DEV/Prod**: never `throw` conditionally on `__DEV__`—use non-throw logging or consistent handling.

Example pattern (state-guard + correct callback isolation):
```js
function onChunkDebug(response, chunk, error) {
  // Don’t mis-route errors once the chunk is already errored/aborted.
  if (chunk.status === 'errored') return;
  triggerErrorOnChunk(response, chunk, error);
}

function flushUserEvents(events) {
  for (let i = 0; i < events.length; i++) {
    try {
      events[i]();
    } catch (e) {
      // Ensure one callback failure doesn’t break later phases.
      reportRecoverableError(e);
    }
  }
}
```

Adopting this prevents hydration/stream coherence issues, avoids incorrect error routing, and reduces “one callback breaks everything” failure modes.