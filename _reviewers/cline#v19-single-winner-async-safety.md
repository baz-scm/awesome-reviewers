---
title: Single-Winner Async Safety
description: 'When multiple async operations can overlap, ensure correctness by making
  the system **single-winner** and **identity-safe**:


  1) **Claim before await** for any “pending resolver” or “pending action”.'
repository: cline/cline#v19
label: Concurrency
language: TypeScript
comments_count: 7
repository_stars: 70885
---

When multiple async operations can overlap, ensure correctness by making the system **single-winner** and **identity-safe**:

1) **Claim before await** for any “pending resolver” or “pending action”.
- Set/clear the shared handle *synchronously*, then `await` attachment/delivery/prep.
- Later arrivals must observe the claimed/cleared state and route as follow-ups.

```ts
// Before: leaving pendingResolve set across await allowed a second submission to “win”.
// After: claim synchronously.
const resolve = this.pendingAskResolve;
if (!resolve) return false;
this.pendingAskResolve = undefined; // claim winner immediately

const hasAttachments = !!(images?.length || files?.length);
try {
  if (hasAttachments && deliverAttachments) {
    await deliverAttachments(() => /* still valid for this attempt */ true);
  }
} catch {
  // deliver failure should not leave the run suspended
}
resolve(prompt ?? "");
return true;
```

2) **Serialize async writes/state transitions per entity** (session/id/task) when order matters.
- Chain writes on a per-session promise queue (or equivalent) so teardown/cancel writes cannot be overwritten by in-flight “running”/“idle” transitions.
- Add guards at the moment the write starts (not when it’s merely scheduled).

3) **Capture the exact target before any async gap**.
- If you will update “the message just created”, capture its index/ID/ts immediately, then update that captured target later.
- Avoid re-finding via non-unique predicates after `await`, which can drift to a newer item if other operations complete first.

4) **Make teardown/cancellation prevent late mutations**.
- Don’t share mutable buffers/state between overlapping executions; capture per-execution state at start.
- Ensure late callbacks and background children can’t keep the host/process alive indefinitely; proactively drop inherited resources/listeners after settlement.

Adopting these rules prevents the recurring classes of bugs shown here: late-writer overwrites, wrong-target updates after await, double-resolve races, and teardown-resistant background work.