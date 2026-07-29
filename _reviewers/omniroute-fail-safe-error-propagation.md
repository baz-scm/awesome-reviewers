---
title: Fail Safe Error Propagation
description: 'Establish an error-handling standard that prevents crashes/hangs, preserves
  root errors, and makes recovery bounded and verifiable.


  Guidelines:

  - Catch safely: prefer `catch (err: unknown)` and narrow before reading fields.'
repository: diegosouzapw/OmniRoute
label: Error Handling
language: TypeScript
comments_count: 9
repository_stars: 33162
---

Establish an error-handling standard that prevents crashes/hangs, preserves root errors, and makes recovery bounded and verifiable.

Guidelines:
- Catch safely: prefer `catch (err: unknown)` and narrow before reading fields.
- Propagate failures to consumers: for streams/transforms, call `controller.error(err)` (not enqueue/continue) and perform deterministic teardown/abort.
- Fail safe on corrupted/unknown inputs: when runtime data may be corrupted, never throw from “read/execute” paths; fall back to a default and keep stricter validation only on writes.
- Bounded fallback/retry: only retry transient connection/dispatcher errors; cap attempts; respect remaining timeout budget.
- Retry guard for request bodies: if the body is non-replayable (stream/Blob), do not retry.
- Don’t shadow the root error: cleanup/rollback failures must not replace the original exception.
- Don’t silently misclassify: when a status code is ambiguous (e.g., 403), decide validity based on explicit evidence (message/body patterns) and cover with tests.

Example (SSE transform fail propagation + streaming semantics):
```ts
return new TransformStream({
  transform(chunk, controller) {
    try {
      // parse/process...
    } catch (err) {
      // Propagate and abort the SSE pipeline
      controller.error(err);
    }
  }
});
```

Example (guarded retry with non-replayable body check):
```ts
const bodyUnknown = options.body as unknown;
const isBodyStream =
  bodyUnknown && typeof bodyUnknown === 'object' &&
  (typeof (bodyUnknown as any).getReader === 'function');
const maxAttempts = isBodyStream ? 1 : 2;

for (let attempt = 0; attempt < maxAttempts; attempt++) {
  try {
    return await undiciDirect(input, { ...options, dispatcher });
  } catch (e) {
    const code = (e as { code?: string }).code;
    if (code === 'ECONNREFUSED' || String(e).includes('fetch failed')) continue;
    throw e;
  }
}
```