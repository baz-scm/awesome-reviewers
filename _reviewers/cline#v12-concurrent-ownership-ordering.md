---
title: Concurrent Ownership & Ordering
description: When async work overlaps, you must prevent stale continuations from mutating
  newer state. Enforce ownership and ordering per logical entity (session/tab/request),
  and make cancellation/deadlines first-class.
repository: cline/cline#v12
label: Concurrency
language: TypeScript
comments_count: 12
repository_stars: 70872
---

When async work overlaps, you must prevent stale continuations from mutating newer state. Enforce ownership and ordering per logical entity (session/tab/request), and make cancellation/deadlines first-class.

**Standard**
1. **Claim ownership before awaiting**: If an operation depends on being “the current one” (answering a pending question, starting a transition), capture/claim synchronously, then do async work. Later submissions must route to the follow-up path.
2. **Serialize side effects per key**: For read-modify-write or state updates that must not interleave (e.g., persisting status), chain/queue operations per entity key so “teardown/final” wins.
3. **Re-validate after awaits**: After any `await`, re-check a cheap validity predicate (e.g., state machine status, “still starting”, “still current”) before touching disposed resources or sending commands.
4. **Never wait forever**: Any connected-client callback/approval/pending response must have an explicit deadline and cleanup path when the owner is gone.
5. **Abort-aware retries/sleeps**: Backoff sleeps and retry attempts must be interruptible by the same abort/cancel signal, and any “fresh” attempt that resolves after abort must be immediately cancelled/closed.
6. **Close resources on late completion**: If an operation times out, ensure late completions (e.g., late `connect()`) don’t leak by closing/disconnecting.

**Example: claim-before-delivery**
```ts
async function resolvePendingAskQuestion(
  prompt: string | undefined,
  images?: string[],
  files?: string[],
  deliverAttachments?: (isCurrent: () => boolean) => Promise<void>,
) {
  const resolve = pendingAskResolve;
  if (!resolve) return false;

  // Claim synchronously so no second submission can resolve the same question.
  pendingAskResolve = undefined;

  const hasAttachments = !!(images?.length || files?.length);

  if (hasAttachments && deliverAttachments) {
    // Validate currentness inside delivery; if not current, delivery no-ops.
    await deliverAttachments(() => /* re-check current attempt id */ true);
    // The core can choose whether to echo locally; important part is ownership.
  }

  // Resolve the claimed question.
  setTurnPhase("streaming");
  resolve(prompt ?? "");
  return true;
}
```

**Example: per-entity serialization (teardown must win)**
```ts
// Pseudocode: chain per sessionId
const perSession = new Map<string, Promise<void>>();
function enqueue(sessionId: string, work: () => Promise<void>) {
  const prev = perSession.get(sessionId) ?? Promise.resolve();
  const next = prev.then(work).finally(() => {
    // Optional cleanup when idle
  });
  perSession.set(sessionId, next.then(() => undefined));
  return next;
}

async function persistStatus(sessionId: string, status: string, shuttingDown: boolean) {
  await enqueue(sessionId, async () => {
    if (shuttingDown && isNonTerminal(status)) return;
    await persistence.writeStatus(sessionId, status);
  });
}
```

If you apply these rules consistently, you eliminate the class of bugs shown in the discussions: out-of-order state overwrites, late async actions touching disposed objects, indefinite waits, and leaked/undercancelled retries.