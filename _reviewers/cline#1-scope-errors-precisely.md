---
title: Scope errors precisely
description: 'Catch and handle only the specific failure you intend to address; don''t
  let a broad try/catch or generic recovery path swallow unrelated causes or apply
  the wrong remedy. Several bugs came from overly coarse error handling: a git helper
  labeled every failure "check your authentication," even for `ls-files` or `worktree
  add` errors that have nothing to do...'
repository: cline/cline#1
label: Error Handling
language: TypeScript
comments_count: 11
repository_stars: 71024
---

Catch and handle only the specific failure you intend to address; don't let a broad try/catch or generic recovery path swallow unrelated causes or apply the wrong remedy. Several bugs came from overly coarse error handling: a git helper labeled every failure "check your authentication," even for `ls-files` or `worktree add` errors that have nothing to do with credentials; a PR-status reader let an unrelated git lookup invalidate a shared `gh` availability cache for every workspace; a skills installer fell back to a different installation method (with different semantics) for any CLI failure, including missing Git or genuine auth errors, instead of only the case the fallback was meant to fix; a credential-hint helper silently degraded to a generic message whenever its input facts didn't match, instead of preserving the specific guidance when possible. In each case the fix was to narrow the catch/condition to the exact case being handled, log or surface the original diagnostic detail (exit code, stderr, specific exception type) even when the user-facing message must be sanitized, and let anything else propagate or fail with its own accurate context.

This also means:
- Never collapse distinct failure classes (timeout vs. auth vs. not-found vs. malformed-input) into one bucket if the response to each should differ (e.g., retry eligibility, user messaging, cache invalidation).
- Compute success/failure classification once in a shared helper when multiple call sites need the same judgment, so the rule can't drift between them.
- Any fire-and-forget or detached async operation (background commits, stdin writes, stream listeners) must have an explicit error handler attached — a missing `.catch()` or error listener turns a specific, recoverable failure into either an unhandled rejection/crash or a silently lost error that never reaches the user or logs.

```ts
// Bad: every git failure gets the same diagnosis
catch {
  throw new Error("Check Git authentication, permissions, and repository state.");
}

// Better: only the call that can fail that way gets that message;
// others propagate with their own detail, and diagnostics are preserved for logs.
catch (error) {
  logger.debug(`git ${args[0]} failed: ${error.stderr ?? error.message}`);
  throw new Error(`git ${args[0]} failed (exit ${error.code}).`);
}
```