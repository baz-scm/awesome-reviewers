---
title: Async State Ownership
description: 'When async operations overlap, never let stale work overwrite or “double-resolve”
  logical state. Adopt these rules:


  1) Claim/own synchronously before awaiting'
repository: cline/cline#v3
label: Concurrency
language: TypeScript
comments_count: 10
repository_stars: 70863
---

When async operations overlap, never let stale work overwrite or “double-resolve” logical state. Adopt these rules:

1) Claim/own synchronously before awaiting
- If there is exactly one valid resolver (e.g., “pending ask question”, “pending capability reply”), capture the resolver promise/handler into a local variable and mark it consumed *before* any `await`.

2) Gate side-effects with generation/currentness
- Use a per-entity token (generation/epoch/“status is still starting”) so callbacks can safely no-op when the owner changed.

3) Serialize per logical entity
- For overlapping writers (same session id, same checkpoint message association, same persisted status row), chain/queue updates per key rather than relying on “last completion wins”.

4) Always time out indeterminate waits
- Any path where an owner may disappear must include capability-appropriate deadlines and cleanup.

5) Cleanup on settle/cancel/fallback
- If you settle a promise early (fallback timeout), remove listeners and release inherited resources so background activity can’t keep the process alive or corrupt buffers.

Code pattern (claim-before-await + generation guard)
```ts
// Example: a single pending resolver (pendingAskResolve-like)
async function resolvePending(
  pending: { current?: (text: string) => void },
  generationRef: { current: number },
  deliverAttachments?: (isCurrent: () => boolean) => Promise<void>,
) {
  const resolve = pending.current;
  if (!resolve) return false;

  // Claim synchronously
  pending.current = undefined;
  const generation = generationRef.current;

  const isCurrent = () =>
    generation === generationRef.current && pending.current === undefined;

  if (deliverAttachments && !isCurrent()) return true; // already superseded
  if (deliverAttachments) {
    await deliverAttachments(isCurrent);
  }

  // Only the claimed resolver completes; stale callbacks can’t replace it.
  resolve("" /* or text */);
  return true;
}
```

Applying this mindset typically prevents:
- late writers overwriting teardown state,
- retries stacking listeners,
- wrong message hashes being attached due to out-of-order commits,
- overlapping “pending question” resolutions,
- indefinite waits after unregister/disconnect,
- resource leaks from fallback settlements.