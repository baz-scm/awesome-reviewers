---
title: Guard async state across await gaps
description: A huge share of concurrency bugs in this codebase come from code that
  checks a condition, then `await`s something (an RPC, a lock, remote config, a file
  write), and acts on the stale result without re-checking whether the world changed
  during that gap. Teardown can start mid-turn, an account/mode switch can land mid-rebuild,
  a record can be deleted or...
repository: cline/cline#|sleep 4
label: Concurrency
language: TypeScript
comments_count: 14
repository_stars: 70979
---

A huge share of concurrency bugs in this codebase come from code that checks a condition, then `await`s something (an RPC, a lock, remote config, a file write), and acts on the stale result without re-checking whether the world changed during that gap. Teardown can start mid-turn, an account/mode switch can land mid-rebuild, a record can be deleted or superseded mid-connect, a status write can be overtaken by a later one, or a cancel can arrive while provisioning is in flight — and the resumed code, unaware, proceeds as if nothing happened (overwriting a `cancelled` status with `running`, replacing a live session with a stale one, deleting a sandbox a user is now using, firing a callback for a question someone already answered, etc.).

To prevent this class of bug:
- Treat every `await` as a point where shared state may have changed. Re-validate the precondition immediately before the side-effecting step that follows an await, not just once at entry. If teardown/cancellation/supersession can start mid-operation, add an explicit check right before the action that must not run afterwards (see turns re-checking `session.shuttingDown` after `markTurnRunning`, or a cloud-task start re-checking `isStale()` before every subsequent await).
- Use a generation/epoch counter (or an equivalent AbortController/token) that is bumped whenever the operation's premise is invalidated (scope change, newer request for the same reason, teardown). Capture the generation before the async work starts and compare it after each await; discard the result if it no longer matches, rather than trusting a boolean checked once at the top.
- When an operation must not be interleaved with a conflicting one (status writes, account switches, session rebuilds, host replacement), serialize them by chaining onto a single pending promise (`pendingX = pendingX.then(() => doWork())`) instead of relying on flags that can be read stale between two awaits.
- When replacing or tearing down a live resource, build/validate the replacement first and only release the old one once the replacement has safely taken its place (or once it's confirmed the old one no longer owns the slot) — never leave a window with neither in place, and never let the old resource's cleanup clobber a newcomer that already took over.
- Add a regression test that deliberately holds one operation mid-flight (e.g. with a blocked promise) while triggering the conflicting event, and asserts the final state is correct — these races are invisible without a test that forces the interleaving.