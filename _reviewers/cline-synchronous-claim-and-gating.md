---
title: Synchronous Claim and Gating
description: In async/concurrent code, establish the operation’s ownership and validity
  *before* the first `await`, and ensure every continuation checks that it is still
  the active owner. Also make required ordering explicit (chain/await when later logic
  depends on it) and always clean up resources when you settle.
repository: CLINE/cline
label: Concurrency
language: TypeScript
comments_count: 8
repository_stars: 70839
---

In async/concurrent code, establish the operation’s ownership and validity *before* the first `await`, and ensure every continuation checks that it is still the active owner. Also make required ordering explicit (chain/await when later logic depends on it) and always clean up resources when you settle.

Apply this as a standard:
1) **Claim first, then await.** If two events can target the same “pending” logical operation (e.g., pending question, pending start, pending commit message update), capture the resolver/target and clear/mark it as claimed synchronously before any async work.
2) **Use a captured token/version.** Store the current attempt id (or resolver reference) in a local variable, and after awaits, only act if the token still matches (or if the claim is still yours).
3) **Don’t move invariant writes into unordered background tasks.** If some later step reads a value you’re about to write (e.g., a checkpoint hash used immediately by attempt completion UI/state), either keep the original awaited flow or explicitly chain so the dependent step runs after the write.
4) **Register handlers once; gate by state and lifecycle.** Avoid stacking `onData`/`onResize`-style listeners across retries. Ensure callbacks no-op after exit/dispose, and clear/gate any stored state.
5) **Settle and clean up subprocess/resources.** If you settle on `exit`, release inherited pipes/listeners (or other handles) so the host doesn’t remain alive waiting for grandchildren.

Example (pending resolution claim pattern):
```ts
async function resolvePendingAsk(
  pending: { requestId: string; resolve: (text: string) => void } | null,
  text: string,
  deliverAttachments?: (isCurrent: () => boolean) => Promise<void>,
  isCurrent: () => boolean,
): Promise<boolean> {
  if (!pending) return false;

  // Claim synchronously: prevent a second submission from also resolving.
  const claimed = pending;
  pending = null;

  const hasAttachments = false; // compute from args
  if (hasAttachments && deliverAttachments) {
    const stillMine = () => isCurrent() /* and/or token match */;
    await deliverAttachments(stillMine);
  }

  // Act only for the claimed attempt.
  if (isCurrent()) {
    claimed.resolve(text);
    return true;
  }
  return true; // already claimed; follow-up can no longer replace it
}
```

Adopt this whenever you see: “await in a function that resolves/cancels/updates shared pending state”, “background promise that later code expects to be completed”, “listeners registered in a retry path”, or “process lifecycle depends on IO handles.”