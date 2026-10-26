---
title: Deterministic Error Handling
description: 'Make all error handling deterministic at async boundaries: never allow
  failures to become unhandled rejections, silent hangs, or incorrectly broad retries.'
repository: cline/cline#v27
label: Error Handling
language: TypeScript
comments_count: 8
repository_stars: 70892
---

Make all error handling deterministic at async boundaries: never allow failures to become unhandled rejections, silent hangs, or incorrectly broad retries.

Standards:
1) Catch both sync exceptions and promise rejections at async boundaries
- If you call a function in a `.then(...)` callback, wrap the whole callback body so a thrown error is handled (not just rejected promises).
- Avoid “fire-and-forget” promises unless they are explicitly caught/logged.

2) For background/detached work, route failures through the same failure path
- If you detach (e.g., `p.then(...)` without `await`), attach `.catch(...)` that logs/records and preserves old semantics (don’t accidentally turn prior “silent fail” into “unhandled rejection”).

3) Retry only when error classification proves it’s safe
- Do not blanket-mark whole operations retryable on ambiguous errors like timeouts; timeouts can mean “client stopped waiting” rather than “provider transient failure”.
- Keep retry budgets and phases distinct (stream vs request vs whole-turn), and don’t override existing retry policies unless you can prove the semantics.

4) Persistence/recovery: acknowledge success only after confirmation; never drop pending state on failure
- For durable queues/batches or “abandoned resource” cleanup, keep pending work on failure and retry later.
- Only remove/settle state after the control plane/storage confirms the operation succeeded.

Code example (catch sync throws inside `.then`):
```ts
export function spawnInProjectSandbox(...): ChildProcess {
  const handle = new SandboxedProcess();

  void loadMxc()
    .then((mxc) => {
      // Any throw here must be caught by the same failure path
      return mxc.spawn({ /* ... */ });
    })
    .then(
      (sandboxed) => {
        handle.attach(sandboxed); // may throw: must be covered by the catch below
      },
      (error) => {
        handle.fail(toFailure(error));
      },
    )
    .catch((error) => {
      // Covers sync exceptions thrown during attach/pipe setup
      handle.fail(toFailure(error));
    });

  return handle as unknown as ChildProcess;
}
```

And (example: don’t detach without a catch):
```ts
// Bad: unhandled rejection if commit fails
checkpoint.commit().then((hash) => update(hash));

// Good:
void checkpoint.commit()
  .then((hash) => update(hash))
  .catch((err) => {
    logger.warn('Failed to create checkpoint', err);
    // preserve existing behavior: don’t change user-visible state unless intended
  });
```

Apply this consistently across: checkpoints/metadata writes, sandbox/worker attach pipelines, transport send loops, and any retry/recovery logic. This reduces both user-visible stalls and correctness issues where retries happen for the wrong reason.