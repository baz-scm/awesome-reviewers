---
title: Precise, non-silent failure handling
description: 'Every error path must be handled deliberately: nothing should escape
  as an unhandled rejection, and no failure should be collapsed into the wrong bucket
  or silently treated as success.'
repository: cline/cline?ref=main
label: Error Handling
language: TypeScript
comments_count: 12
repository_stars: 70980
---

Every error path must be handled deliberately: nothing should escape as an unhandled rejection, and no failure should be collapsed into the wrong bucket or silently treated as success.

1. Attach an explicit handler to every promise or stream you don't directly await. A detached `.then(onSuccess)` that omits a rejection handler (or whose `onSuccess` itself can throw) becomes an unhandled rejection that can crash the host. Use `.then(onSuccess).catch(onError)` so both the original rejection and any exception thrown while handling success are caught:
```ts
// Bad: a rejected spawn is caught, but a throw inside attach() is not.
promise.then(attach, onError);

// Good: both paths are covered.
promise.then(attach).catch(onError);
```
The same applies to error/stdin listeners on child processes and streams (e.g. attach `stream.on("error", …)` whenever you write to it) and to calls like `kill()` that can themselves throw or reject — wrap them and route the failure through the same error-reporting path instead of letting it surface as a bare exception.

2. Classify failures by their actual cause before deciding how to handle them — don't let a coarse catch-all decide behavior. A timeout doesn't prove a request is safe to retry; a generic "command failed" doesn't prove a tool is missing; a missing git ref doesn't prove "not a repository" versus "some other fatal error." Match on the specific signal (exit code, stderr text, exception type) and handle only the cases you've actually verified, letting everything else propagate so it isn't misdiagnosed or silently converted into the wrong fallback (e.g. switching install methods, granting a retry budget, or returning a default value) for errors that don't warrant it.

3. Never let a failed operation report success or fall through as if nothing happened. If a step fails, either propagate the error, record it as an explicit failure state that downstream logic can check, or roll back any state you already changed in anticipation of success (e.g. restore a saved preference, revert an optimistic UI flag). Avoid "best effort" catches that swallow an error without a trace — even logging-only catches should be deliberate and documented, not accidental silences that hide real bugs.

Applying these three checks during review — unhandled rejections, overbroad error classification, and silent success-on-failure — catches the majority of error-handling regressions before they reach production.