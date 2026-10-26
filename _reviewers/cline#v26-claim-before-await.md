---
title: Claim Before Await
description: 'When shared async state drives side effects (UI updates, offers, persistence,
  rebuild/config, retries), do two things to prevent interleaving bugs:


  1) **Claim/record ownership synchronously (no awaits first).**'
repository: cline/cline#v26
label: Concurrency
language: TypeScript
comments_count: 7
repository_stars: 70893
---

When shared async state drives side effects (UI updates, offers, persistence, rebuild/config, retries), do two things to prevent interleaving bugs:

1) **Claim/record ownership synchronously (no awaits first).**
- Before any `await`, make the operation “the winner” by clearing/advancing the shared pointer/flag/version.
- Pattern: capture the current token/handle, set the shared state to “claimed” (or advance epoch), then perform async work.
- This prevents a second concurrent completion from resolving/replacing the same pending action (e.g., duplicate ask-question resolution, stale UI epochs).

2) **Serialize or order side effects per entity.**
- For per-session/per-request/per-file/per-epoch state, ensure only one write sequence can win:
  - chain writes on a per-session promise queue,
  - use staged/activate epochs for replacements,
  - ensure rebuild/task transitions supersede correctly,
  - preserve request order when multiple hub reads can be in flight.
- Never “update the newest thing later” from a background promise; capture the exact target at creation time (message index/id, file inode/signature, runtime object) or serialize.

3) **Use interleaving-safe external mutations.**
- File pruning/unlinking must be “remove-if-unchanged” (rename aside + conditional delete, or equivalent compare-and-swap), not “stat then rm” across awaits.

4) **Make loops and delays abort-aware.**
- Retries and backoff sleeps must stop promptly on cancellation signals; don’t release shared locks early.

Example (claim-before-await for a shared pending operation):
```ts
// shared state
let pendingResolve: ((text: string) => void) | undefined;

async function resolvePending(
  text: string,
  deliverAttachments?: () => Promise<void>,
): Promise<boolean> {
  const resolve = pendingResolve;
  if (!resolve) return false;

  // Claim synchronously: prevent any concurrent call from also resolving.
  pendingResolve = undefined;

  const hasAttachments = !!deliverAttachments;
  if (hasAttachments) {
    try {
      await deliverAttachments!();
      // avoid double-echo if attachments are delivered via a different path
    } catch (e) {
      // decide policy: fall back to text-only or surface error
    }
  }

  // State is already claimed; safe to complete after awaits.
  resolve(text);
  return true;
}
```

Checklist for code reviews in this category:
- ✅ Do we clear/advance the shared pointer/version/epoch **before** the first `await`?
- ✅ Are side effects serialized or ordered per entity (session id, plugin epoch, message target)?
- ✅ Does background work update the **exact captured target**, not a later “search the latest” result?
- ✅ Are external mutations (files/processes) guarded against interleaving (remove-if-unchanged / token checks)?
- ✅ Are waits/retries/backoffs abort-aware, and are locks held correctly across cancellation?

Applying this standard prevents the common failure modes seen in the discussions: double-resolves, stale UI/state serving, lost or overwritten status writes, and out-of-order persistence after concurrent checkpoint/rebuild operations.