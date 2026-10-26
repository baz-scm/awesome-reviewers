---
title: Robust async error routing
description: 'When handling async work, never let errors fall through as “rare” no-ops
  or escape into unhandled rejections—also avoid misleading recovery decisions. Coding
  standard:'
repository: cline/cline#v16
label: Error Handling
language: TypeScript
comments_count: 11
repository_stars: 70882
---

When handling async work, never let errors fall through as “rare” no-ops or escape into unhandled rejections—also avoid misleading recovery decisions. Coding standard:

1) **Route all failure paths to the same handler**
- Don’t assume exceptions thrown inside callbacks passed to `.then()` are caught by a rejection handler; they may bypass the intended failure path.
- Use a single chain pattern: `promise.then(onSuccess).catch(onError)` (or wrap `onSuccess` in try/catch) so errors thrown during attach/stream wiring are reported and the synthetic process/state is closed.

```ts
function spawnAndWire(): ChildProcessLike {
  const handle = new SandboxedHandle();

  void loadDependency()
    .then((dep) => dep.spawn({ /*...*/ }))
    .then((child) => {
      // If attach throws, it must hit the same catch.
      handle.attach(child); 
    })
    .catch((err) => {
      handle.fail(new Error(`Couldn't keep command inside sandbox: ${String(err)}`));
    });

  return handle;
}
```

2) **Classify errors precisely; recover only on verified signals**
- Treat “missing”/“not found” as a specific, confirmed class of failure—don’t convert arbitrary failures into fake deletions or fake success.
- For retries, ensure the retry decision is based on the error’s semantics (e.g., timeouts are not automatically whole-turn retryable).
- For health/startup probes, distinguish “starting/indeterminate” from true invalid responses; indeterminate windows should not fatally abort.

3) **Preserve invariants and UI truth**
- Never emit/record “success” (or make success-visible state changes) before the underlying operation’s result is guaranteed.
- If background work is intentionally non-blocking, still handle rejections (log/telemetry) and prevent leaving UI artifacts that imply completion with missing data.

4) **Avoid silent defaults on unreadable/corrupt state**
- If configuration read fails (torn/corrupt settings), don’t silently flip behavior off; distinguish “absent” vs “unreadable” and warn/record so users understand why safeguards may be disabled.

5) **Prevent false measurements/telemetry**
- Clear observation timers and pending “runtime samples” when the process/sandbox never actually started.

Adopting these rules prevents: orphaned live work, hung pending calls, unhandled rejections, misleading recovery outputs, and incorrect retry/health decisions—directly improving error handling quality across the codebase.