---
title: Isolate secondary failures
description: Every promise that is not awaited by its caller (background `.then()`
  chains, detached cleanup, `kill()`/`cancel()` calls, telemetry or notice emission,
  dispose hooks) must have an explicit failure handler. An unguarded rejection from
  "fire-and-forget" work surfaces as an unhandled rejection and can crash or hang
  the whole process, not just the operation...
repository: cline/cline#`sleep 4`
label: Error Handling
language: TypeScript
comments_count: 17
repository_stars: 70979
---

Every promise that is not awaited by its caller (background `.then()` chains, detached cleanup, `kill()`/`cancel()` calls, telemetry or notice emission, dispose hooks) must have an explicit failure handler. An unguarded rejection from "fire-and-forget" work surfaces as an unhandled rejection and can crash or hang the whole process, not just the operation that failed.

Just as important: secondary or supporting work (logging, telemetry, user-facing notices, cleanup) must never be allowed to overwrite, discard, or get conflated with the primary error or state a caller/user depends on. If recording a failure, emitting a notice, or running `ctx.onDispose` cleanup itself throws, catch it, log it, and continue surfacing the original error untouched — don't let the secondary failure become the reported outcome, and don't let a thrown listener inside an `emit()` replace the real failure.

```ts
// Bad: rejection from detached work is unhandled, and a cleanup failure can
// replace the real error.
checkpointTracker.commit().then(async (hash) => {
	await updateMessage(hash);
});

try {
	await createCheckpoint(...);
} catch (error) {
	await recordFailure(error); // if this throws, the original error is lost
	throw error;
}

// Good: detached work is guarded, and secondary failures are isolated.
checkpointTracker.commit().then(
	async (hash) => updateMessage(hash),
	(error) => logger.error("checkpoint commit failed", error),
);

try {
	await createCheckpoint(...);
} catch (error) {
	await recordFailure(error).catch((recordError) =>
		logger.warn("failed to record checkpoint failure", recordError),
	);
	throw error; // the original error always wins
}
```

Apply this whenever code spawns detached promises, calls `kill()`/`dispose()`/cleanup on a failure path, or emits telemetry/notices around an operation that can itself fail: give every detached promise a rejection handler, and make sure failures in logging/telemetry/cleanup/notification never suppress, replace, or get blamed for the error the caller actually needs to see.