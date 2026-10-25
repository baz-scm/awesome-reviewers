---
title: Robust Async Error Invariants
description: 'Adopt a single standard for error handling in async/control-flow code:


  1) **Never let setup/teardown exceptions escape their owner**

  - Ensure errors thrown inside helper callbacks (e.g., stream piping, attach, pipe
  setup) are caught and routed through the same failure path as rejected promises.'
repository: cline/CLINE
label: Error Handling
language: TypeScript
comments_count: 9
repository_stars: 70839
---

Adopt a single standard for error handling in async/control-flow code:

1) **Never let setup/teardown exceptions escape their owner**
- Ensure errors thrown inside helper callbacks (e.g., stream piping, attach, pipe setup) are caught and routed through the same failure path as rejected promises.
- Avoid patterns like `promise.then(fn, onError)` when `fn` can throw; prefer `promise.then(fn).catch(fail)`. 

2) **Prevent unhandled rejections from “cleanup” operations**
- If a cleanup API may throw (e.g., kill/terminate), wrap it and convert to the module’s normal `fail/record` mechanism.
- Never ignore returned cleanup promises if they can reject.

3) **Enforce lifecycle invariants explicitly (no “rare null” fallthrough)**
- When reaching a state that violates safety/lifecycle assumptions (e.g., session artifacts still missing after a guard), **fail fast** (throw) instead of letting code fall into another path that can orphan/replace live work.
- During shutdown, reject new work rather than accepting and silently dropping it.

4) **Avoid silent fail-open on configuration/settings reads**
- Distinguish “file absent” vs “file unreadable/corrupt.” If unreadable, surface a warning or preserve the last known good value so protection doesn’t silently disable.

5) **Make retry/recovery semantics-driven**
- Do not automatically treat all provider failures (notably timeouts) as whole-turn retryable.
- Gate retries on explicit “safe-to-retry” semantics; timeouts often mean “client stopped waiting,” not “work didn’t happen.”

6) **Best-effort telemetry must not interrupt the primary flow**
- Wrap telemetry calls so unexpected exceptions don’t abort inference/operations.

Example pattern

```ts
function runWithFail<T>(p: Promise<T>, fail: (err: unknown) => void): void {
  void p.then(() => {}).catch(fail);
}

// 1) Catch exceptions thrown inside attach
const handle = createHandle();
void loadSandbox()
  .then((mxc) => mxc.spawn(config))
  .then((sandboxed) => {
    // attach may throw (stream setup, environment checks, etc.)
    handle.attach(sandboxed);
  })
  .catch((err) => {
    handle.fail(err instanceof Error ? err : new Error(String(err)));
  });

// 2) No unhandled kill/release rejections
async function safeKill(proc: { kill(): void; dispose(): void }) {
  try {
    proc.kill();
  } catch (e) {
    // Route through the same error reporting path, don't throw/reject uncaught.
    report(e);
  } finally {
    proc.dispose();
  }
}

// 3) No rare-state fallthrough
if (liveSession && !liveSessionCanStartRun) {
  await ensureSessionPersisted(liveSession);
  if (!liveSession.artifacts) {
    // Invariant violated: do not fall through to replacement path.
    throw new Error('Live session missing persisted artifacts; refusing to replace');
  }
}
```

Adopting these rules prevents hangs/unhandled rejections, preserves session/task safety, and ensures retry/recovery/telemetry behave according to their real semantics rather than incidental error shape.