---
title: Precise failure classification
description: Error handling must distinguish between genuinely different failure causes
  instead of collapsing them into one generic catch, message, or outcome. Before writing
  a catch block, ask what specific conditions can land there and whether they deserve
  different treatment — a timeout is not the same as a permission error, "not a git
  repository" is not the same as...
repository: cline/cline#|sleep 4
label: Error Handling
language: TypeScript
comments_count: 17
repository_stars: 70979
---

Error handling must distinguish between genuinely different failure causes instead of collapsing them into one generic catch, message, or outcome. Before writing a catch block, ask what specific conditions can land there and whether they deserve different treatment — a timeout is not the same as a permission error, "not a git repository" is not the same as a corrupted object, a missing executable is not the same as a missing working directory, and an unparsable response is not the same as an unreachable server. Collapsing these loses the information a user or on-call engineer needs to act, and can cause the wrong recovery path to run (e.g. treating a transient "still starting" response as fatal, or retrying a budget-exhausting operation because a timeout was treated as universally retryable).

Concretely:
- Narrow `catch` blocks to the specific error shapes you intend to handle; check exit codes together with stderr/message content when the same exit code can mean different things (e.g. git's exit 128 means "not a repository" only when stderr confirms it — any other fatal error should propagate as "unknown", not be assumed clean or absent).
- Never let a failure silently present as success (e.g. a sync code path must apply the same `finishReason === "error"` guard as the async path; a tool executor returning `success: false` must be treated as a failure even without `isError`).
- Never let a non-fatal condition abort a whole operation when a narrower fallback exists (e.g. a shell-environment capture that exceeds a size limit should log and fall back to default inheritance, not fail `startSession` outright).
- Ensure every async failure path is actually observed: a rejected `.then()` handler that can itself throw needs `.catch()`, not just an error callback on the initial promise; a write to a pipe/stream whose other end closed needs an `error` listener so Node doesn't raise it as an uncaught/unhandled rejection.
- Preserve the original cause when wrapping errors for display or telemetry — redact secrets if needed, but don't erase the distinguishing details (command, exit code, phase) that let the real problem be diagnosed later.

Example of narrowing a catch instead of a blanket message:
```ts
// Bad: every git failure gets the same misleading message.
catch (error) {
  throw new Error("Check Git authentication, permissions…");
}

// Good: only truly matching conditions are treated specially.
const NOT_A_REPOSITORY = 128;
try {
  return gitFacts(parseGitStatus(await run(...)));
} catch (error) {
  if (errorCode(error) === NOT_A_REPOSITORY && /not a git repository/i.test(stderrOf(error))) {
    return undefined; // genuinely no repo
  }
  return "unknown"; // any other fatal error stays unknown, never "clean"
}
```