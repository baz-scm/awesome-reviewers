---
title: Use ownership and guards
description: 'When async operations can overlap, avoid “late completion overwrites”
  and “stale callbacks win” by enforcing an explicit ownership/validity contract.

  '
repository: cline/cline#v28
label: Concurrency
language: TypeScript
comments_count: 11
repository_stars: 70892
---

When async operations can overlap, avoid “late completion overwrites” and “stale callbacks win” by enforcing an explicit ownership/validity contract.

**Standards**
1) **Claim synchronously before awaiting** for any replaceable promise/work (pending questions, sends, in-flight operations). Once claimed, later submissions must route as follow-ups instead of re-resolving.
2) **Guard every write-back** with a **generation/epoch/revision token** (per session/task/render). In-flight callbacks must verify their token is still current before they publish results.
3) **Serialize teardown/persistence** so teardown/status transitions can’t be reordered by concurrent writes (chain writes on a per-session queue; ensure “teardown lands last”).
4) **Deadline + cancellation must include cleanup**: if you time out or abort, ensure late completions either (a) do not mutate shared state, and/or (b) clean up external resources (disconnect, drop pipes/listeners) so the host won’t hang or leak.
5) **Fail fast on ownership loss**: if the requester/owner disconnected, do not wait forever—return a user-visible continuation/fallback immediately.

**Code pattern (claim before await)**
```ts
async function resolvePendingAsk(opts: {
  prompt?: string;
  images?: string[];
  files?: string[];
  deliverAttachments?: (isCurrent: () => boolean) => Promise<void>;
}) {
  const hasAttachments = !!(opts.images?.length || opts.files?.length);
  const resolve = pendingAskResolve;
  if (!resolve) return false;

  // Claim immediately so a second submit can't resolve the same question.
  pendingAskResolve = undefined;

  const responseText = opts.prompt ?? "";
  const shouldEchoLocally = !hasAttachments;

  if (hasAttachments && opts.deliverAttachments) {
    await opts.deliverAttachments(() => pendingAskResolve === undefined /*isCurrent*/);
    // If attachments were delivered, core/local echo should not also send them.
  }

  if (shouldEchoLocally) {
    // append user feedback / local echo
  }

  // Drive the state machine forward exactly once.
  setTurnPhase("streaming");
  resolve(responseText);
  return true;
}
```

Apply this checklist anywhere you see:
- `await` between “choose target” and “commit result”,
- shared mutable state written by multiple async paths,
- background promises that later “update previous UI/persistence”.

(Doing so consistently prevents the class of bugs repeatedly fixed across sends, plugin/UI epochs, session status persistence, refresh/prune races, and attachment/delivery resolution.)