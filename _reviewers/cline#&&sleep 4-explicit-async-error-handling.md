---
title: Explicit async error handling
description: 'Every asynchronous operation — promise chains, spawned child processes,
  event emitters, streams, sockets — must have its failure path explicitly handled.
  Never leave a promise, event listener, or stream without an error handler: a rejection
  or exception that escapes becomes an unhandled rejection or uncaught exception that
  can crash or hang the host...'
repository: cline/cline#&&sleep 4
label: Error Handling
language: TypeScript
comments_count: 14
repository_stars: 70980
---

Every asynchronous operation — promise chains, spawned child processes, event emitters, streams, sockets — must have its failure path explicitly handled. Never leave a promise, event listener, or stream without an error handler: a rejection or exception that escapes becomes an unhandled rejection or uncaught exception that can crash or hang the host process. This applies especially to fire-and-forget code: detached `.then()` chains, background writes, `kill()` calls on child processes, and stdin/stdout streams on subprocesses all need an attached `.catch()` or `on("error", …)` handler that logs the failure and leaves the system in a safe state, rather than one that silently disappears or propagates to the process. For example, prefer `promise.then(attach).catch(fail)` over `promise.then(attach, onError)`, since the latter only covers rejection of the outer promise, not an exception thrown inside `attach` itself.

When an error is caught, preserve its real cause instead of collapsing distinct failure modes into one generic bucket. An exit code, a timeout, a closed stream, and an HTTP/response status can each mean something different (e.g. exit 128 means "not a repository" only when stderr confirms it; `ENOENT` can mean a missing executable or a missing working directory; a 503 "starting" response is not the same as an invalid response). Classify based on the actual signal available, not assumptions, so retries, fallbacks, and telemetry attribute the failure correctly. Avoid speculative blanket overrides (e.g. treating all timeouts as retryable, or silently switching to a different transport/strategy on any failure) — verify the specific condition before changing behavior, and keep diagnostic detail intact for cases that don't match the known-safe condition.