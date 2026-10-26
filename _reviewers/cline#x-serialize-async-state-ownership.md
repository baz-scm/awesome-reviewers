---
title: Serialize Async State Ownership
description: When multiple async operations can overlap, require explicit ownership/ordering
  so late completions can’t overwrite newer intent, and ensure waits are bounded/cleaned
  up.
repository: cline/cline#x
label: Concurrency
language: TypeScript
comments_count: 9
repository_stars: 70861
---

When multiple async operations can overlap, require explicit ownership/ordering so late completions can’t overwrite newer intent, and ensure waits are bounded/cleaned up.

Apply these rules:
1) **Claim before `await`** for single-consumer “pending” actions.
   - Synchronously take the pending token/handler, then `await` delivery.
   - Any later concurrent submission must route elsewhere (follow-up) instead of resolving the same pending item.

2) **Serialize mutations per resource** (session/run/plugin/task/etc.).
   - Chain writes/updates on a per-entity promise queue or lock.
   - Add teardown/shutdown guards at the point the write actually starts, not when it is merely scheduled.

3) **Capture the exact mutation target before background work**.
   - Don’t re-find “the latest” record after an `await` (global searches create TOCTOU bugs when overlaps occur).

4) **Bound and clean up**.
   - Avoid indefinite waits when ownership can disappear; fail fast or use capability-appropriate deadlines.
   - On cancellation/timeout, settle and dispose inherited resources (timers/pipes/listeners) so the process doesn’t hang.

Example pattern (claim + capture + serialize):
```ts
// per resource serialization
const queues = new Map<string, Promise<void>>();
function enqueue<T>(key: string, work: () => Promise<T>): Promise<T> {
  const prev = queues.get(key) ?? Promise.resolve();
  let resolveNext!: () => void;
  const next = new Promise<void>((r) => (resolveNext = r));
  queues.set(key, prev.then(() => next));
  return prev
    .then(work)
    .finally(() => {
      resolveNext();
      // optionally delete when idle
    });
}

// single-consumer claim before await
async function resolvePending(pending: { fn?: (x: string) => void }, prompt: string) {
  const claim = pending.fn;
  if (!claim) return false;
  pending.fn = undefined; // claim synchronously

  const responseText = prompt; // capture
  await deliverAttachmentsSafely();
  claim(responseText);
  return true;
}

// background commit: capture target synchronously
async function updateCheckpoint(messageState: any) {
  const idx = messageState.findIndex(m => m.say === 'checkpoint_created');
  if (idx === -1) return;
  const target = messageState.at(idx);
  enqueue('checkpoint', async () => {
    const commitHash = await commitGit();
    // update exactly `target` (or re-check identity) instead of re-searching
    messageState.updateAt(idx, { lastCheckpointHash: commitHash });
  });
}
```
This standard prevents the “late writer wins” class of bugs, overlapping background mutations, and cancellation/leak issues across the codebase.