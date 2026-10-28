---
title: Classify errors before recovering
description: 'When a `catch` block decides what to do next, don''t assume every error
  it intercepts has the same cause — inspect the specific signal (exception type,
  exit code, status, or message pattern) and pick a recovery path that matches it.
  A blanket fallback applied to "any failure" routinely does the wrong thing for cases
  it wasn''t meant to handle: retrying every...'
repository: cline/cline#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
label: Error Handling
language: TypeScript
comments_count: 23
repository_stars: 70976
---

When a `catch` block decides what to do next, don't assume every error it intercepts has the same cause — inspect the specific signal (exception type, exit code, status, or message pattern) and pick a recovery path that matches it. A blanket fallback applied to "any failure" routinely does the wrong thing for cases it wasn't meant to handle: retrying every provider timeout as if it were transient, treating any non-zero git exit as "not a repository," falling back to an archive install for missing-git or auth errors instead of just missing git, invalidating an unrelated cache because one git command failed, or silently disabling a capability check just because an auxiliary lookup didn't match. Prefer an explicit allow-list of recognized "benign" failure signatures over a reject-list, and let anything unrecognized propagate instead of being absorbed into a generic fallback.

Pair this with two related habits:
- **Never leave a promise unhandled.** Any async call that isn't directly awaited (a detached `.then()`, a fire-and-forget `commit()`/`kill()`, a listener callback) needs an explicit `.catch()` or try/catch that routes the error into the same failure-reporting path as everything else. An unhandled rejection in a hook, socket listener, or background task can crash the whole host process instead of just failing the one operation.
- **Never report or persist success when the underlying action failed.** If a write, commit, mode switch, or sync throws, roll back any optimistic state change (don't keep a new mode/flag that was never actually applied) and don't mark a result "completed" when the operation actually errored or aborted.

```ts
// Bad: assumes every rejection means "not a repo", and the caller
// never learns about a different fatal failure.
try {
  await run("git", ["status"], cwd);
} catch {
  return undefined; // silently treated as "no repository"
}

// Good: only the recognized signature is treated as benign;
// anything else propagates so the real cause surfaces.
try {
  await run("git", ["status"], cwd);
} catch (error) {
  if (isNotARepositoryError(error)) return undefined;
  return "unknown";
}

// Bad: fire-and-forget write with no error handler.
tracker.commit().then((hash) => recordHash(hash));

// Good: failure is caught and reported instead of becoming an
// unhandled rejection.
tracker.commit().then(
  (hash) => recordHash(hash),
  (error) => logger.error("checkpoint commit failed", error),
);
```