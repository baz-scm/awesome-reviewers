---
title: Precise failure classification
description: When code treats a failure as benign, expected, or recoverable, that
  decision must be based on a narrow, explicit match against the known causes — never
  a catch-all default. Anything that falls outside the known conditions is a real
  failure and must propagate (or be logged/reported) rather than being silently reinterpreted
  as success, "not applicable", or...
repository: cline/cline#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
label: Error Handling
language: TypeScript
comments_count: 10
repository_stars: 70965
---

When code treats a failure as benign, expected, or recoverable, that decision must be based on a narrow, explicit match against the known causes — never a catch-all default. Anything that falls outside the known conditions is a real failure and must propagate (or be logged/reported) rather than being silently reinterpreted as success, "not applicable", or an empty/missing result.

This surfaces repeatedly:
- A git exit code of 128 only means "not a repository" when stderr actually says so; any other fatal error must be reported as unknown, not collapsed into the same case (discussion 5).
- `git show` failing should only be treated as "this side doesn't exist" when the error matches specific "missing object/path" patterns (`does not exist`, `invalid object name`, etc.); an unrelated failure such as hitting an output-size limit must propagate as an error instead of rendering as a fake deletion (discussion 14).
- A blanket fallback (e.g., switching install strategies, or skipping Hub starting-state handling) must not apply to every error class — only to the specific precondition/config failure it was designed for; other failures (auth, network, "still starting") need their own distinct handling, not reuse of the same recovery path (discussions 21, 25).
- Regex/string matching against error messages to detect a specific condition (e.g., "session not found", "HTTP 404") must be verified against what the real failure actually produces, not just what a test mock returns (discussion 24).
- A reported status (e.g., `"completed"`) must reflect the actual terminal outcome (`finishReason`) rather than being hardcoded or assumed when a known failure path (`finishReason === "error"`) was dropped (discussion 31).

Equally important: once an error is correctly identified as a genuine failure, it must never vanish. Don't fire-and-forget a promise without a `.catch` (a detached checkpoint commit became an unhandled rejection with no user-visible signal, discussion 37); don't let a `.then(success, onError)` miss exceptions thrown synchronously inside the success handler — use `.then(success).catch(onError)` so both paths are covered (discussion 16); and when a recovery handler itself fails, requeue/report the original failure before invoking the error callback, and guard that callback so a throwing logger can't escape and crash the caller (discussion 42). A baseUrl or other user-provided value passed to `new URL(...)` without a try/catch can throw outside of any expected error path and should be validated/caught explicitly (discussion 46).

In short: write an explicit allow-list of conditions that justify treating a failure as the "normal" case, propagate everything else, and make sure every promise chain and recovery path has a terminal error handler so failures are always visible instead of silently disappearing or being misreported as success.