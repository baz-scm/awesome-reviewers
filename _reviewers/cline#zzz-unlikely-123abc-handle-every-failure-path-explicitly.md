---
title: Handle every failure path explicitly
description: 'Treat failure detection and propagation as part of the contract, not
  an afterthought. Two recurring bug classes keep recurring in review:


  1. **Detached/background work with no rejection handler.** Any `.then()`/async call
  that isn''t awaited by its caller (checkpoint commits, sandbox process attach, socket
  frame parsing, MCP stdin writes, process kill) must...'
repository: cline/cline#zzz-unlikely-123abc
label: Error Handling
language: TypeScript
comments_count: 11
repository_stars: 71035
---

Treat failure detection and propagation as part of the contract, not an afterthought. Two recurring bug classes keep recurring in review:

1. **Detached/background work with no rejection handler.** Any `.then()`/async call that isn't awaited by its caller (checkpoint commits, sandbox process attach, socket frame parsing, MCP stdin writes, process kill) must have an explicit `.catch`/`try-catch` that routes the error into the same failure path a synchronous caller would see (fail the operation, log, or close the resource). `.then(onSuccess, onError)` only catches a rejected promise, not an exception thrown inside `onSuccess`; prefer `.then(onSuccess).catch(onError)` so both are covered. Never let one of these become an unhandled rejection that can crash or hang the host process.

   ```ts
   // risky: exception inside attach() bypasses onError, and exit races inside attach can crash the process
   void loadMxc().then(attach, onError);

   // better: both branches funnel through the same error handler
   void loadMxc().then(attach).catch(onError);
   ```

2. **Success assumed from "no exception" rather than checked from the actual result.** Some APIs report failure through a return value (`{ success: false }`, a `finishReason: "error"` on an otherwise-resolved promise) instead of throwing. Code that only wraps calls in try/catch — and ignores these explicit failure signals — will record or display success for an operation that actually failed. Always check both: catch thrown errors AND inspect result fields that signal failure before deciding an operation succeeded.

When you do handle a failure, preserve its real cause instead of collapsing every error into one generic message or blindly deciding it's retryable/transient — a timeout, a credential error, and a malformed response are different problems and should be diagnosable and treated differently downstream (while still redacting sensitive details like credentials from user-facing text). Add a regression test for the specific failure path you're fixing, not just the happy path.