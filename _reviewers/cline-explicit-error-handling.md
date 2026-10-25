---
title: Explicit Error Handling
description: 'Adopt a standard that prevents misleading state, lost root causes, and
  unhandled async failures—especially in recovery/timeout paths.


  Rules:

  1) Handle both rejection and exceptions in promise chains'
repository: CLINE/CLINE
label: Error Handling
language: TypeScript
comments_count: 13
repository_stars: 70837
---

Adopt a standard that prevents misleading state, lost root causes, and unhandled async failures—especially in recovery/timeout paths.

Rules:
1) Handle both rejection and exceptions in promise chains
- If you attach via `.then(x, onError)`, also guard exceptions thrown inside `x` (setup/stream wiring/attach). Prefer `.then(attach).catch(...)` when attach can throw.

2) Never leave critical async work unobserved
- Avoid fire-and-forget `.then(...)` without a `.catch(...)` when failure changes UI/state or invariants. Either `await` inside the existing try/catch, or attach an explicit catch that logs and/or reports state.

3) Cleanup/cancel timers on the error path
- If you arm timers/observers before an async operation, ensure spawn/connect failures cancel or suppress the observation to avoid false “ran/exited” metrics or late callbacks.

4) Preserve error meaning; don’t silently widen retryability
- Timeouts/session-lost must be classified based on the actual transport/provider semantics. Don’t blanket-mark timeouts as whole-turn retryable; preserve the original timeout phase/reason and diagnostic fields.

5) Never “silently disable” safety
- If protection depends on reading config, distinguish “missing file” vs “corrupt/unreadable file”. If the read fails, either fail closed with an explicit warning or return a user-visible warning while keeping protection behavior consistent with the last known valid value.

6) Route all async stream/write failures into the correct failure handler
- Attach stdin/pipe error listeners (EPIPE/EOF on Windows) so the host doesn’t crash and so the request fails fast with the annotated reason.

Example: replace a fragile promise chain that can throw during attach
```ts
const handle = new SandboxedProcess();
void loadMxc()
  .then((mxc) => mxc.spawn(/* ... */))
  .then((sandboxed) => handle.attach(sandboxed))
  .catch((error: unknown) => {
    // Ensures both spawn rejection AND attach exceptions are handled.
    const reason = error instanceof Error ? error.message : String(error);
    handle.fail(new Error(`Sandbox failed: ${reason}`));
  });
```

Example: avoid unhandled commit failures
```ts
try {
  await this.say("checkpoint_created");
  const commitHash = await this.checkpointTracker.commit();
  await this.messageStateHandler.updateClineMessage(
    /* index */, { lastCheckpointHash: commitHash }
  );
} catch (e) {
  Logger.warn("checkpoint commit failed", e);
  // Preserve previous behavior: show that no hash is available without breaking the run.
}
```

Example: cancel observation timer on spawn failure
```ts
let timer: NodeJS.Timeout | undefined;
try {
  timer = setTimeout(report, observationMs);
  timer.unref?.();
  const child = spawn(/* ... */);
  // ...
} catch (e) {
  if (timer) clearTimeout(timer);
  // Emit only spawn failure; do not emit an exited:false runtime sample.
  throw e;
}
```

Applying these rules consistently will reduce orphaned state, false telemetry, lost attribution (timeouts), and unhandled promise rejections across run/recovery/sandbox/plugin execution flows.