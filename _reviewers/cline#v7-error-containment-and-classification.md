---
title: Error containment and classification
description: 'Coding standard for the team:


  1) Contain async errors end-to-end

  - If you start async work and then continue in another callback/continuation, ensure
  both (a) rejection and (b) exceptions thrown inside the continuation are caught
  and routed to the same controlled error path.'
repository: cline/cline#v7
label: Error Handling
language: TypeScript
comments_count: 10
repository_stars: 70865
---

Coding standard for the team:

1) Contain async errors end-to-end
- If you start async work and then continue in another callback/continuation, ensure both (a) rejection and (b) exceptions thrown inside the continuation are caught and routed to the same controlled error path.
- Never create “detached” promises inside try/catch blocks unless you attach a handler that records/logs failures.

2) Synthetic/adapter abstractions must fail in a single, deterministic way
- For wrapper “process” handles (sandboxed hooks/commands), ensure cleanup paths (kill/abort/dispose) never throw out of the wrapper. Route non-zero/timeout/kill errors into the wrapper’s own error reporting.

3) Always listen for stream/IPC write failures
- Any child/hook/IPC stdin writes can fail asynchronously (e.g., EPIPE/EOF on Windows). Add an `error` listener on the stream so it can’t become an uncaught host exception; annotate it on the final reported failure.

4) Classify failures conservatively (no fake success)
- Only treat an operation as “missing/not found” when the underlying tool explicitly signals that condition. Unexpected errors (size limits, timeouts, serialization issues, transport bugs) must propagate as real errors rather than being mapped into plausible-but-wrong states.
- Do not broaden retry eligibility by blanket rules (e.g., “timeouts are always retryable”). Preserve existing phase/budget semantics and add tests for retry safety.

Example pattern (process/sandbox wrapper)
```ts
function spawnWrapped(config: SpawnConfig): ChildLike {
  const handle = new SandboxedProcess();

  // Make sure exceptions thrown during attach are caught as well.
  void loadSandbox()
    .then((sandbox) => {
      try {
        handle.attach(sandbox); // may throw during stream setup
      } catch (e) {
        handle.fail(normalizeError(e));
      }
    })
    .catch((e) => {
      handle.fail(new Error(`Sandbox failed: ${String(e)}`));
    });

  return handle;
}

class SandboxedProcess extends EventEmitter {
  attach(sandbox: MxcProcess) {
    // Always attach stdin error absorption
    sandbox.standardInput?.on('error', (err) => {
      this.fail(normalizeError(err));
    });
    // ...then wire stdout/stderr
  }

  kill() {
    try {
      this.process?.kill();
    } catch (e) {
      // Never allow cleanup to escape as an unhandled rejection/uncaught exception.
      this.fail(normalizeError(e));
    }
  }
}
```

5) Recovery must be bounded and state-safe
- If you retry/recover (session lost, restart windows, timeouts), re-handshake/replay only under the exact recognized “lost” conditions, and ensure retries are limited and don’t corrupt/duplicate side effects.

If implemented consistently, these rules prevent the most common failure modes seen in the reviewed code: unhandled promise/stream errors, hangs, misleading “missing”/“successful” interpretations, and unsafe retry behavior that repeats side effects.