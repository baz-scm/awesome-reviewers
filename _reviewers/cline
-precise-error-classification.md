---
title: Precise error classification
description: When catching or branching on an error, match the specific, verifiable
  condition that justifies the chosen behavior — never fall back to a broad catch-all
  that silently absorbs unrelated failures. A generic handler (e.g., "check Git authentication"
  for every git command failure, `exit 128` always meaning "not a repository", any
  `git show` failure treated as...
repository: 'cline/cline

  '
label: Error Handling
language: TypeScript
comments_count: 16
repository_stars: 70942
---

When catching or branching on an error, match the specific, verifiable condition that justifies the chosen behavior — never fall back to a broad catch-all that silently absorbs unrelated failures. A generic handler (e.g., "check Git authentication" for every git command failure, `exit 128` always meaning "not a repository", any `git show` failure treated as a missing file, a `TimeoutError` always granted a fresh retry budget, or a failed sync tool call defaulting to `status: "completed"`) hides the real cause, produces misleading user-facing messages, corrupts telemetry, or lets destructive fallbacks run for the wrong reason (e.g. switching from a git-backed install to a raw archive download on *any* git failure, including proxy/cert issues it can't actually fix). Instead, check the precise signal — stderr text, exit code plus message, error type/instance, or an explicit status field — before deciding the response, and let anything that doesn't match that signal propagate unchanged.

```ts
// Bad: any error on this side is treated as "file missing"
const text = await git(["show", `${rev}:${path}`]).catch(() => undefined);

// Good: only the specific "no such object" errors count as missing;
// anything else (e.g. a maxBuffer limit) propagates as a real failure
const MISSING_OBJECT = /does not exist|not in index|unknown revision/i;
const text = await git(["show", `${rev}:${path}`]).catch((error) => {
	if (MISSING_OBJECT.test(String(error))) return undefined;
	throw error;
});
```

Equally important: never let an async failure go unhandled. A `.then(onSuccess)` without a paired rejection handler, a fire-and-forget promise with no `.catch()`, or a stream/socket `error` listener that isn't attached will surface as an unhandled rejection or uncaught exception and can crash the host process, while swallowing the one piece of context (stderr, exit code, cause) a user or developer needed to diagnose the problem. Every promise chain and event emitter must have an explicit failure path — logged, reported, or rethrown with full context — rather than relying on an enclosing handler that doesn't actually cover it.

```ts
// Bad: a rejection here becomes an unhandled rejection
void spawnSomething().then(onSuccess);

// Good: failure path is explicit and attributed
void spawnSomething().then(onSuccess, (error) => handleFailure(error));
```