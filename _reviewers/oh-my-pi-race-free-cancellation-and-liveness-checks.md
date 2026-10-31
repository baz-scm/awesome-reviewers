---
title: Race-free cancellation and liveness checks
description: When wiring an `AbortSignal` (or any cancellation token) into async work
  — spawning processes, reading files, racing I/O — eliminate every window where a
  cancellation could be missed or where stale resource state could be misjudged as
  live.
repository: can1357/oh-my-pi
label: Concurrency
language: JavaScript
comments_count: 15
repository_stars: 37317
---

When wiring an `AbortSignal` (or any cancellation token) into async work — spawning processes, reading files, racing I/O — eliminate every window where a cancellation could be missed or where stale resource state could be misjudged as live.

1. No gap between the abort check and the listener. Always call `signal?.throwIfAborted()` immediately before registering the `abort` listener, with no `await` in between; otherwise an abort fired during that gap is silently lost.

```js
signal?.throwIfAborted();
const child = Bun.spawn([...]);
const onAbort = () => { /* kill child/tree */ };
signal?.addEventListener("abort", onAbort, { once: true });
```

2. Race every async step against the signal, don't just attach a listener to the outermost await. A `fs.stat`, a file read, or a probe command can each stall; wrap them with a helper that rejects as soon as the signal fires, not only once the whole operation settles:

```js
async function untilAborted(promise, signal) {
  if (!signal) return promise;
  promise.catch(() => {}); // avoid unhandled rejection if abort wins
  const aborted = Promise.withResolvers();
  const onAbort = () => aborted.reject(signal.reason);
  signal.addEventListener("abort", onAbort, { once: true });
  try {
    signal.throwIfAborted();
    return await Promise.race([promise, aborted.promise]);
  } finally {
    signal.removeEventListener("abort", onAbort);
  }
}
```

3. On cancellation, terminate the whole process tree a child may have spawned, not just the immediate child (process-group/session kill on POSIX, tree-kill on Windows), and document known gaps (e.g. double-forked or reparented descendants) rather than silently leaving them unhandled.

4. Never judge whether a resource's owner is still alive using a reusable handle alone. A bare PID can be reused by an unrelated process, and the same PID can mean different things across hosts/containers sharing a filesystem. Build liveness/ownership checks from a composite, scoped identity (host/machine + namespace + pid + process start time) and validate every part before treating an owner as dead; treat ambiguous or unscoped identities as "possibly alive" rather than risking a false "dead" classification that triggers unsafe cleanup of a resource still in use by another process.

5. Bound memory and avoid holding shared mutable state across concurrent accesses: cap captured output, use exclusive per-process record files instead of a single file multiple processes could race to write/rename, and keep cleanup scoped to resources this process/scope actually owns.

Apply this checklist whenever a PR introduces cancellation, cross-process coordination, or cleanup-of-stale-state logic: identify every await that could stall, confirm there's no check-then-register gap, and confirm ownership/liveness decisions can't be fooled by identifier reuse or cross-host collisions.