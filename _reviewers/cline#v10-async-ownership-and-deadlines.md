---
title: Async Ownership and Deadlines
description: 'When async work overlaps (retries, disconnects, replacements, rebuilds,
  timeouts), you must ensure:


  1) Claim ownership before awaiting

  - If multiple submissions/events can target the same “pending” outcome, synchronously
  “claim” the pending resolver/slot before starting any awaited steps (e.g., attachment
  delivery). Otherwise a later submission can resolve...'
repository: cline/cline#v10
label: Concurrency
language: TypeScript
comments_count: 10
repository_stars: 70869
---

When async work overlaps (retries, disconnects, replacements, rebuilds, timeouts), you must ensure:

1) Claim ownership before awaiting
- If multiple submissions/events can target the same “pending” outcome, synchronously “claim” the pending resolver/slot before starting any awaited steps (e.g., attachment delivery). Otherwise a later submission can resolve the same pending item and cause missing/duplicated side-effects.

2) Publish only if still eligible (generation/identity)
- Capture a generation/token (or equivalent session/operation identity) when starting the async operation.
- After awaiting, verify the operation is still the current eligible one before publishing results or writing state.
- If detachment/explicit cancellation exists, ensure *all* resolution paths honor it (requested owner and fallback/alternate owner).

3) Always bound liveness: deadlines + cancellation + cleanup
- Never allow “forever waits” for callbacks/owners that might have disconnected.
- Add request-type-specific deadlines.
- On cancel/timeout/settlement, cleanup: remove listeners, clear timers, close/flush inherited resources, and ensure fallback settlement can’t keep processes alive.

4) Constrain concurrency safely
- Use a max-parallelism mechanism that limits in-flight work but still runs all queued items (don’t drop excess work when enforcing concurrency).

Practical pattern (adapt as needed)
```ts
// Example: pending-resolution with claim + deadline + eligibility check.
let pending: { token: number; resolve: (v: string)=>void } | null = null;
let currentToken = 0;

export async function resolvePendingAsk({ text, images }: {
  text?: string; images?: string[];
}): Promise<boolean> {
  // 1) Claim synchronously.
  const claimed = pending;
  if (!claimed) return false;
  pending = null;

  const myToken = ++currentToken; // capture eligibility for publish
  const deadlineMs = 10_000;

  const deliver = async () => {
    // 2) Bounded async secondary steps.
    const hasAttachments = (images?.length ?? 0) > 0;
    if (hasAttachments) {
      await withTimeout(
        sendAttachments(images!),
        deadlineMs,
        "delivering attachments",
      );
    }
    // 3) Publish only if still eligible.
    if (myToken !== currentToken) return; // replaced/cancelled
    options.setTurnPhase?.("streaming");
    claimed.resolve(text ?? "");
  };

  try {
    await deliver();
  } finally {
    // 4) Cleanup on success/failure (listeners/timers removed elsewhere,
    // but ensure this function doesn’t leave anything running).
  }

  return true;
}

function withTimeout<T>(work: Promise<T>, ms: number, what: string): Promise<T> {
  let t: ReturnType<typeof setTimeout> | undefined;
  const timeout = new Promise<never>((_, reject) => {
    t = setTimeout(() => reject(new Error(`${what} exceeded ${ms}ms`)), ms);
  });
  return Promise.race([work, timeout]).finally(() => t && clearTimeout(t));
}
```
Adopt this mindset for: hub capability requests, UI “pending” interactions, plugin call wrappers, subprocess lifecycle handling, and rebuild/scheduling transitions. The goal is consistent: no stale publication, no indefinite waits, no leaked resources, and bounded concurrency.