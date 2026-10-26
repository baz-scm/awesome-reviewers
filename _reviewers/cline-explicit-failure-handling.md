---
title: Explicit failure handling
description: 'Every operation that can fail must have its failure path treated as
  deliberately as its success path. Three recurring gaps keep surfacing in review:


  1. **Unhandled rejections/exceptions from "success" callbacks.** A `.then(onSuccess,
  onError)` only catches a rejection of the original promise, not a throw inside `onSuccess`
  itself; a bare `.then(fn)` on a...'
repository: cline/cline
label: Error Handling
language: TypeScript
comments_count: 20
repository_stars: 70886
---

Every operation that can fail must have its failure path treated as deliberately as its success path. Three recurring gaps keep surfacing in review:

1. **Unhandled rejections/exceptions from "success" callbacks.** A `.then(onSuccess, onError)` only catches a rejection of the original promise, not a throw inside `onSuccess` itself; a bare `.then(fn)` on a detached/background promise has no handler at all. Both leave real failures as uncaught exceptions that can crash the host process. Prefer `.then(onSuccess).catch(onError)`, and make sure every "fire-and-forget" promise (background git pushes, stdin writes, detached hooks, timer callbacks) has an attached `.catch`/error listener even when nothing awaits it.

```ts
// Bad: a throw inside attach() becomes an unhandled rejection.
loadMxc().then(attach, onError);

// Good: failures from either the load or the attach are caught.
loadMxc().then(attach).catch(onError);
```

2. **Success inferred from "it resolved" instead of the actual outcome.** Don't report `status: "completed"`, mark a plugin "ready", or reset a retry/failure counter just because a call returned — check the real signal first: `finishReason`, exit code, HTTP status, non-empty content, or an explicit `ok`/`skipReason` field. An empty result, a truncated response, or an error-shaped payload that merely didn't throw must still be classified as a failure.

3. **Secondary/non-critical work must not corrupt the primary result.** Telemetry, logging, cache invalidation, and cleanup should run in their own try/catch (or dedicated error boundary) so a throwing listener or a failed best-effort write can never flip an otherwise-successful operation into a failure, crash the process, or silently replace the original error with an unrelated one. When an error does occur, preserve and propagate the original cause (not a generic message) so callers and telemetry see what actually happened, and distinguish "nothing to report" from "something went wrong" rather than collapsing both into the same branch.

Apply this checklist whenever reviewing new async code: every promise has a catch, every outcome is checked against its real status field, and no auxiliary concern can mask or mutate the primary operation's true result.