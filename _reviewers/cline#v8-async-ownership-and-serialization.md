---
title: Async Ownership And Serialization
description: 'When handling concurrent/overlapping async work, never let “late” completions
  overwrite newer state or resolve the same pending item twice. Enforce three rules:'
repository: cline/cline#v8
label: Concurrency
language: TypeScript
comments_count: 8
repository_stars: 70867
---

When handling concurrent/overlapping async work, never let “late” completions overwrite newer state or resolve the same pending item twice. Enforce three rules:

1) Decide ownership synchronously (before any await)
- For any “pending”/“in flight” unit (ask question, status transition, checkpoint association), claim it (set/clear the resolver) immediately, then do awaits.
- Route later submissions to a follow-up/queue path instead of reusing the same resolver.

2) Serialize shared mutable writes per key
- For state that can be written by multiple async paths (shutdown vs idle transitions, polls vs forced refresh, status persistence), chain operations per entity key (sessionId/taskId/recordId) so the intended winner lands last.

3) Capture update targets before async boundaries
- If you must update a previously emitted UI/log/message after an async operation, capture the exact handle/index (or generation-qualified reference) immediately; don’t “re-find” by searching after awaits (which can associate with a newer message).

Practical patterns (adapt as needed):

```ts
// 1) Claim before await (pending resolver)
async function resolvePending(pending: { current?: (v: string) => void }, prompt: string) {
  const resolve = pending.current;
  if (!resolve) return false;
  pending.current = undefined; // claim synchronously

  // now safe to await attachment delivery
  await deliverAttachmentsIfAny();
  resolve(prompt ?? "");
  return true;
}

// 2) Serialize per key (chained persistence writes)
const perKeyWriteTail = new Map<string, Promise<void>>();
function enqueueWrite(key: string, job: () => Promise<void>): Promise<void> {
  const tail = perKeyWriteTail.get(key) ?? Promise.resolve();
  const next = tail.then(job, job);
  perKeyWriteTail.set(key, next);
  return next;
}

// 3) Capture target before async work
const createdIndex = findIndexOfCreatedMessageNow();
const commitPromise = checkpointTracker.commit();
await say('checkpoint_created');
commitPromise.then((hash) => {
  // update exactly the message created for THIS commit
  updateMessage(createdIndex, { lastCheckpointHash: hash });
});
```

Apply this checklist to review requests:
- Are there any awaits between “check” and “act” on shared state?
- Can two async paths write the same logical field out of order?
- Are we using late lookups (search-by-type/label) after async completion instead of captured handles?
- Do cancellations/teardowns guard against displaced/live replacements via per-key generation or start-time guards?

If answers suggest races, require serialization/claiming/capture-by-reference before approving the change.