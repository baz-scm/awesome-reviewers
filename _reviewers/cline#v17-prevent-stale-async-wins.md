---
title: Prevent stale async wins
description: When async work overlaps, the biggest correctness risk is *late or out-of-date
  work still mutating shared state or resolving a single-use decision*. Standardize
  on patterns that make authority explicit and preserve ordering.
repository: cline/cline#v17
label: Concurrency
language: TypeScript
comments_count: 10
repository_stars: 70883
---

When async work overlaps, the biggest correctness risk is *late or out-of-date work still mutating shared state or resolving a single-use decision*. Standardize on patterns that make authority explicit and preserve ordering.

Do:
- **Serialize state writes per key** (session/task/request id) so teardown/cancel paths can’t be overwritten by in-flight transitions.
- **Claim ownership before awaiting** for any “single resolver” (pending ask/question/tool result). After the first claim, later submissions must take the follow-up path or fail fast.
- **Queue/coalesce reads and re-reads** so results apply in the order they were requested (don’t let a slower in-flight read or poll overwrite newer state).
- **Bound every wait** (deadlines) and make sleeps/operations **abort-aware**; ensure late completions clean up (e.g., disconnect after a deadline).
- **Capture the exact target before an await** when updating a specific record/message; don’t “re-find” later in a background promise.
- **Use atomic “unchanged” operations** (rename/unlink-if-unchanged) when multiple processes/threads may update the same file.

Example: claim-before-await single-use resolver
```ts
async function resolvePendingAsk(params: {
  pendingResolve: undefined | ((text: string) => void);
  prompt?: string;
  images?: string[];
  deliverAttachments?: (isCurrent: () => boolean) => Promise<void>;
}): Promise<boolean> {
  const resolve = params.pendingResolve;
  if (!resolve) return false;

  // Claim immediately so no other submission can resolve/replace this decision.
  // (Set pendingResolve = undefined in the owning object.)

  const hasAttachments = !!(params.images?.length);
  const prompt = params.prompt ?? "";

  if (hasAttachments && params.deliverAttachments) {
    // After claiming, deliver attachments without allowing a second submission
    // to resolve the same ask.
    await params.deliverAttachments(() => /* isCurrent() token */ true);
    // If delivery fails, fall back to echoing prompt or routing error as policy.
  }

  // Finally resolve the claimed decision.
  resolve(prompt);
  return true;
}
```

Example: per-key serialization for state transitions
```ts
const chains = new Map<string, Promise<void>>();
function runSerial<T>(key: string, work: () => Promise<T>): Promise<T> {
  const prev = chains.get(key) ?? Promise.resolve();
  let next!: Promise<T>;
  next = prev.then(work, work);
  chains.set(key, next.then(() => {}, () => {}).then(() => {
    if (chains.get(key) === prev) chains.delete(key);
  }));
  return next;
}

// Use runSerial(sessionId, () => updateStatus(...)) for every transition write.
```

Outcome: overlapping async operations no longer “win by being late”; authority is enforced via serialization, claiming, ordering, bounded waits, and atomic target selection.