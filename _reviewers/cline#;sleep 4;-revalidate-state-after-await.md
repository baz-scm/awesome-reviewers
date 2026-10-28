---
title: Revalidate state after await
description: 'Many of the hardest-to-reproduce bugs in this codebase come from one
  pattern: code checks a condition or reads shared mutable state, then suspends on
  an `await`, and later acts as if that earlier check/read is still true. A concurrent
  operation — another request, a retry, a reconnect, a reload, a timer, a sibling
  async call — can change the world during the...'
repository: cline/cline#;sleep 4;
label: Concurrency
language: TypeScript
comments_count: 16
repository_stars: 70976
---

Many of the hardest-to-reproduce bugs in this codebase come from one pattern: code checks a condition or reads shared mutable state, then suspends on an `await`, and later acts as if that earlier check/read is still true. A concurrent operation — another request, a retry, a reconnect, a reload, a timer, a sibling async call — can change the world during the suspension, so the resumed code commits a stale decision, overwrites a newer write, double-fires a side effect, or hands a result to the wrong caller.

Guard against this with explicit, cheap mechanisms rather than hoping interleavings don't happen:

- **Claim before you yield.** If an operation must happen at most once (answering a question, resolving a pending callback, consuming a token), claim/clear the shared slot synchronously, *before* the first `await`, not after. A second caller that arrives during the await must see the slot already claimed, so it falls through to a different path instead of double-handling the original.
- **Tag state with a generation/identity, and check it after every await, not before.** When a background operation (refresh, rebuild, reconnect, reload) resumes after I/O, don't assume its target still exists or is still current — compare the live object/generation against what you started with, and drop the write if it's been superseded, replaced, or torn down.
- **Serialize conflicting writers through a single chained queue, not independent awaits.** Two writers racing to update the same resource (a session status, an account switch, a file) should be chained on one promise per key so the later-requested write always lands after the one in flight, rather than finishing based on whichever I/O call happens to return first.
- **Prefer atomic replace-or-fail over check-then-act for external resources.** For files, use rename-aside-then-verify (or compare-and-swap) rather than separate stat/delete calls with a gap between them; for sockets/handles, re-probe or re-subscribe after reconnecting rather than trusting the pre-reconnect state.
- **Release/cleanup only when you still own the slot.** Before tearing down or overwriting a registered resource (a session map entry, a cached host, a lock), check that the entry still points at the object you're cleaning up; if it's already been displaced by a newer instance, leave it alone.

As a concrete shape, an answer-resolution race was fixed by claiming before any async delivery step:

```ts
const resolve = this.pendingResolve
if (!resolve) return false
this.pendingResolve = undefined // a second submission now takes a different path
try {
  await deliverAttachments()
} catch (error) {
  // handle without ever leaving the question unanswered
}
resolve(responseText)
return true
```

Before adding a new await in a path that reads-then-writes shared state, ask: what else could run between the read and the write, and what happens to this code if it does? Add a regression test that holds the await open and fires the competing operation to prove the fix.