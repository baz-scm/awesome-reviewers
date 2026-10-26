---
title: Fail Predictably, Retry Safely
description: 'Adopt a single error-handling rule for all async boundaries: **every
  failure must be captured, classified, and routed to the correct outcome (retry,
  wait, degrade, or fail) without silently changing semantics.**'
repository: cline/cline#v20
label: Error Handling
language: TypeScript
comments_count: 15
repository_stars: 70886
---

Adopt a single error-handling rule for all async boundaries: **every failure must be captured, classified, and routed to the correct outcome (retry, wait, degrade, or fail) without silently changing semantics.**

Apply these standards:
1) **Catch errors at the async boundary (including inside “success” callbacks).** If you attach streams, initialize processes, or create handlers in a `.then(...)`, you must also `.catch(...)` (or `try/catch` around the await) so exceptions don’t become unhandled rejections/hung calls.
2) **No fallthrough after an “ensure/guard” step.** If a guard intended to prevent orphaning/incorrect replacement can’t guarantee required state (e.g., artifacts not persisted), don’t continue into the code path that can replace live state.
3) **Classify retryability—timeouts/aborts/disconnects are not automatically transient.** Don’t grant whole-turn retry budgets or replay actions just because a timeout happened. Only retry when the failure type is known to be recoverable.
4) **Retry/wait only the right states and for the right window.** Example: waiting for “hub connecting” should retry; “session not found” should trigger re-handshake; otherwise return explicit sentinel outcomes (e.g., `unknown`) instead of empty data.
5) **On failures, preserve the user-truth: record failures or keep the last safe content.** Persistence/storage failures must never silently erase or misrepresent results; keep prior state or degrade with an explicit “failed/unrecorded” outcome.

Small pattern to follow (captures exceptions inside attach/initialization):
```ts
void loadMxc()
  .then((mxc) => mxc.spawn(/*...*/))
  .then(
    (sandboxed) => handle.attach(sandboxed),
    (err) => handle.fail(new Error(String(err))),
  )
  .catch((err) => {
    // Covers exceptions thrown inside attach()/setup too.
    handle.fail(err instanceof Error ? err : new Error(String(err)));
  });
```

When implementing any retry or fallback, first answer: **(a)** what error class is it (transient vs non-retryable), **(b)** what state is safe to retry, **(c)** what is the explicit degraded/sentinel output if recovery can’t proceed.