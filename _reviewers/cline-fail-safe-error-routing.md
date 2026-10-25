---
title: Fail Safe Error Routing
description: In error/timeout/recovery flows, ensure every failure (including exceptions
  thrown inside callbacks, stream write failures, and detached promises) is routed
  through the code path that owns reporting/retries/state invariants—never as an unhandled
  rejection/exception and never as a silent fallback.
repository: CLINE/cline
label: Error Handling
language: TypeScript
comments_count: 11
repository_stars: 70839
---

In error/timeout/recovery flows, ensure every failure (including exceptions thrown inside callbacks, stream write failures, and detached promises) is routed through the code path that owns reporting/retries/state invariants—never as an unhandled rejection/exception and never as a silent fallback.

Actionable standards:
1) Catch exceptions in async callback chains
- If you do `promise.then(attach)` where `attach()` can throw (stream setup, socket checks, etc.), use `.then(attach).catch(onError)` (or wrap `attach` in try/catch). Don’t rely on promise rejection handling only.

2) Wrap “stop/kill” paths so shutdown failures can’t escape
- If `kill()`/shutdown can throw synchronously or asynchronously, catch and convert into the same failure reporting mechanism.

3) Handle stream-side async errors (EPIPE/Eof) explicitly
- For subprocess/child-process stdin/stdout/stderr streams, add `stream.on('error', ...)` handlers so Node doesn’t treat it as an uncaught host exception.

4) Clear or cancel timers on spawn/initialization failure
- If you arm observation/censorship timers, cancel them when the process fails to spawn; otherwise you’ll emit false “ran” samples.

5) Never leave detached promises unhandled
- If you start background work with `.then(...)` or similar, attach a `.catch(...)` that logs/telemetry-report within the intended error policy.

6) Keep telemetry side-effects non-interrupting
- Telemetry should be best-effort: failures must not abort inference, execution, or core git/runtime operations.

7) Classify retries/recovery intentionally
- Don’t blanket-mark timeouts or failures as retryable; only retry/recover when the error semantics prove it is transient/appropriate. Add fixture-based tests for retry classification.

Example pattern (spawn + attach failure routing):
```ts
export function spawnSandbox(config: Config): ChildProcess {
  const handle = new SandboxedProcess();
  void loadSandbox()
    .then((sandboxed) => {
      try {
        handle.attach(sandboxed); // may throw
      } catch (e) {
        handle.fail(e instanceof Error ? e : new Error(String(e)));
      }
    })
    .catch((error) => {
      const reason = error instanceof Error ? error.message : String(error);
      handle.fail(new Error(`Couldn't keep this command inside project: ${reason}`));
    });
  return handle as unknown as ChildProcess;
}
```

Example pattern (stdin write error absorption):
```ts
child.stdin?.on('error', (err) => {
  // Record/annotate, but do not let it crash the host process.
  Logger.debug(`stdin write failed: ${(err as Error).message}`);
});
```

These rules directly prevent the recurring failure modes seen in the discussions: unhandled rejections/uncaught exceptions, incorrect or silent fallbacks after initialization/settings reads, and retry/recovery decisions that don’t match the error semantics.