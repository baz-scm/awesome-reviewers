---
title: Graceful Error Recovery
description: When handling failures in async, remote, or multi-step flows, make the
  system degrade safely and keep UI/state consistent with what the server actually
  persisted.
repository: aaif-goose/goose
label: Error Handling
language: TypeScript
comments_count: 4
repository_stars: 51876
---

When handling failures in async, remote, or multi-step flows, make the system degrade safely and keep UI/state consistent with what the server actually persisted.

Apply these rules:

1) Bound remote calls; fall back on hang
- Wrap discovery/fetch operations in a timeout.
- If the call times out or errors, use cached/last-known-good data so user flows don’t stall forever.
- Add tests for “never resolves” cases.

2) Keep optimistic updates reversible and server-aligned
- If you optimistically update local state, ensure every error path either:
  - rolls back the optimistic change, or
  - replaces local state with the known persisted state.
- Do not attempt to “restore” data that may have been destroyed server-side; recovery must match persisted store behavior.

3) Guard destructive operations with preconditions
- Before performing actions that delete/truncate server state, validate required invariants (e.g., required working directory present).
- On precondition failure, return a structured error and avoid destructive side effects.

4) Retry best-effort operations with bounded backoff and clear completion semantics
- For replay/subscription catch-up, retry per item with bounded exponential backoff (and a max attempt count).
- Mark the replay/catch-up as complete only when the required per-item work has succeeded; exhausted failures should remain retryable.

Example pattern (timeout + fallback + consistent state + bounded retry):

```ts
async function withTimeout<T>(p: Promise<T>, ms: number): Promise<T> {
  return await Promise.race([
    p,
    new Promise<T>((_, reject) => setTimeout(() => reject(new Error('timeout')), ms)),
  ]);
}

async function listModelsWithFallback(providerId: string): Promise<string[]> {
  try {
    const live = await withTimeout(
      fetchLiveModels(providerId), // remote call
      4000
    );
    return live;
  } catch {
    return await fetchCachedInventoryModels(providerId); // safe degraded path
  }
}

async function retryEachUri(uris: string[], fn: (uri: string) => Promise<void>) {
  const maxAttempts = 3;
  for (const uri of uris) {
    let attempt = 0;
    while (attempt < maxAttempts) {
      try {
        await fn(uri);
        break; // success for this item
      } catch {
        attempt++;
        if (attempt >= maxAttempts) throw new Error(`exhausted: ${uri}`);
        const backoffMs = Math.min(200 * 2 ** (attempt - 1), 2000);
        await new Promise((r) => setTimeout(r, backoffMs));
      }
    }
  }
}
```

If you follow these principles together, your error handling will be both user-friendly (no hangs), correct (no state divergence), and resilient (retries are bounded and semantics are explicit).