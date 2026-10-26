---
title: Error Boundary Discipline
description: 'At every async boundary, treat errors as first-class: capture both promise
  rejections and exceptions thrown inside callbacks, route them through a single structured
  failure path, and only retry when the error is explicitly eligible (especially don’t
  grant timeouts/aborts extra retry budget).'
repository: cline/cline#v2
label: Error Handling
language: TypeScript
comments_count: 13
repository_stars: 70861
---

At every async boundary, treat errors as first-class: capture both promise rejections and exceptions thrown inside callbacks, route them through a single structured failure path, and only retry when the error is explicitly eligible (especially don’t grant timeouts/aborts extra retry budget).

Practical rules:
1) Wrap callback internals, not just promise outcomes
- Use `.then(fn).catch(handle)` (or `await try/catch`) so exceptions thrown inside `fn` are handled.

2) Never let async failures become unhandled rejections
- If you intentionally detach work, attach a `.catch()` that logs/records the failure with best-effort semantics.

3) Absorb “async surface” write/stream errors that should not crash the host
- If a child/server closes stdin early, install `stdin.on('error', ...)` (or equivalent) to prevent uncaught exceptions; let the normal exit handler produce the primary failure message.

4) Decide retry eligibility by error type/phase, not by blanket rules
- Timeouts/aborts often mean “client stopped waiting,” not that the provider failed transiently—don’t automatically make them whole-turn retryable.
- Preserve structured timeout attribution even if a reason gets serialized to a string.

5) Don’t silently change user-visible behavior on corrupt/unreadable state
- Distinguish “absent” vs “unreadable/torn/corrupt” config; surface a warning or telemetry so a protection/feature doesn’t appear to “turn off” invisibly.

Code example (error boundary):
```ts
export function spawnSandboxSafe(config: ProjectSandboxSpawnConfig) {
  const handle = new SandboxedProcess();

  void loadMxc()
    .then((mxc) => {
      // any exception thrown here must be caught by the catch below
      return mxc.spawn({ /* ... */ });
    })
    .then((sandboxed) => {
      handle.attach(sandboxed); // if attach throws, catch below runs
    })
    .catch((error: unknown) => {
      const reason = error instanceof Error ? error.message : String(error);
      handle.fail(
        new Error(
          `Couldn't keep this command inside your project (${reason}). ` +
          `Turn off the sandbox setting to run anyway.`,
        ),
      );
    });

  return handle as unknown as ChildProcess;
}
```

Apply this checklist in places like: detached background promises, child-process stdin/stdout pipes, transport/session reconnection logic, and retry/telemetry attribution paths.