---
title: Safe Error Propagation
description: 'When implementing error handling across async boundaries (process/sandbox/streams,
  detached promises, retry logic), enforce four rules:


  1) **No unhandled rejections/exceptions**: every promise created via `void x.then(...)`,
  `.then(fn)` without a rejection handler, or background work must have an explicit
  `.catch(...)` (and must route failures into the...'
repository: cline/cline#v22
label: Error Handling
language: TypeScript
comments_count: 6
repository_stars: 70886
---

When implementing error handling across async boundaries (process/sandbox/streams, detached promises, retry logic), enforce four rules:

1) **No unhandled rejections/exceptions**: every promise created via `void x.then(...)`, `.then(fn)` without a rejection handler, or background work must have an explicit `.catch(...)` (and must route failures into the same failure/telemetry path as synchronous errors).
2) **Handle stream write failures**: if you pipe to a child (or worker) stdin/stdout/stderr, attach `error` listeners to the stream objects that can fail asynchronously (not just the child’s `exit/close`).
3) **Retry only when safe**: don’t blanket-mark whole-turn retries as eligible due to broad conditions (e.g., timeouts). Derive retryability from error class + existing retry-budget exhaustion.
4) **Cleanup on failure**: cancel timers and release resources on spawn/rejection paths; never let observation/telemetry timers run after a failed spawn.

Example pattern (covers rules 1,2,4):
```ts
const observation = setTimeout(() => report({ exited:false }), 30_000);
observation.unref?.();

try {
  const child = spawn(cmd, args);

  // Prevent uncaught host exceptions when stdin write fails.
  child.stdin?.on('error', (e) => {
    // Record/annotate; do not throw.
    stdinFailure = e instanceof Error ? e.message : String(e);
  });

  await completedPromise(child); // whatever resolves on close/exit

  clearTimeout(observation);
  report({ exited:true, stdinFailure });
} catch (e) {
  // Spawn/initialization failed => don't emit false “ran 30s” samples.
  clearTimeout(observation);
  throw e;
}
```

Example pattern (rule 3):
- Keep the existing retry-budget checks and only mark retryable when the error is explicitly transient/safe; do **not** override them for timeouts without confirming the request wasn’t processed and that retry won’t duplicate side effects.