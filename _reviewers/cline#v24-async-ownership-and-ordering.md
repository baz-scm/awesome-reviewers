---
title: Async Ownership And Ordering
description: 'When multiple async flows can overlap, make “who owns the right to complete”
  explicit and keep effects ordered.


  Standards:

  1) Claim/own state before awaiting'
repository: cline/cline#v24
label: Concurrency
language: TypeScript
comments_count: 15
repository_stars: 70891
---

When multiple async flows can overlap, make “who owns the right to complete” explicit and keep effects ordered.

Standards:
1) Claim/own state before awaiting
- Immediately mark a pending operation as resolved/owned (e.g., set the resolver to undefined, increment a generation, or record an epoch) before the first await. This prevents a second submission from resolving the same pending item while the first one is still delivering side effects.

2) Serialize work at consistency boundaries
- Any code path that must observe a stable snapshot or ensure “last write wins” must use a queue/lock/chain or “one request at a time” rule, and re-run if something changed while the in-flight operation was running.

3) Ignore stale async replies
- Use a generation/epoch token captured at bind/start time; apply reducer/state updates only if the token still matches when the async call returns.

4) Make cancellation/deadlines explicit
- Don’t leave requests waiting forever: add deadlines appropriate to the request kind, and ensure abort signals propagate through retries/probes.

5) Avoid TOCTOU and async gaps
- If an invariant depends on a value produced asynchronously (commit hash, file contents, pending context), capture the needed target synchronously or serialize commits; for file deletion/updates under concurrent writers, use compare-and-swap style checks (rename+verify/unchanged) rather than “stat then unlink”.

Example pattern (claim before await):
```ts
async function resolvePending(pending: { current?: (x: string) => void },
  text: string, deliverAttachments?: (isCurrent: () => boolean) => Promise<void>) {
  const resolve = pending.current;
  if (!resolve) return false;

  // Claim immediately: a second submission can't resolve the same item.
  pending.current = undefined;

  const hadAttachments = deliverAttachments !== undefined;
  if (hadAttachments) {
    await deliverAttachments(() => pending.current === undefined);
  }

  // Now complete the claimed response.
  resolve(text);
  return true;
}
```

Use this checklist for any new async feature that:
- has “pending” user/agent state,
- triggers multiple overlapping requests (refresh/poll/retry/toggle),
- relies on ordering between UI updates and background work,
- or performs read-modify-write (files, DB rows, shared in-memory maps).
