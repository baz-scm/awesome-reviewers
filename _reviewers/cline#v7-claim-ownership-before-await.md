---
title: Claim Ownership Before Await
description: When multiple async actions can overlap, treat every side-effect as applying
  to a specific “current” entity. Concurrency bugs come from late completions writing
  into newer state.
repository: cline/cline#v7
label: Concurrency
language: TypeScript
comments_count: 13
repository_stars: 70865
---

When multiple async actions can overlap, treat every side-effect as applying to a specific “current” entity. Concurrency bugs come from late completions writing into newer state.

Standard:
1) Claim ownership synchronously (no awaits) before starting any async work that must be exclusive.
2) Validate identity/generation both before and after awaits (generation tokens for binds/retries; session/task ids for status updates).
3) Serialize competing side-effects per key (per session, per run, per checkpoint message) so the intended ordering (e.g., teardown last) is guaranteed.
4) Bound “wait forever” flows with deadlines; on timeout, ensure late completions are cleaned up (disconnect/stop/ignore) rather than leaking or overwriting.
5) Avoid TOCTOU in async resource cleanup; prefer remove-if-unchanged or recheck synchronously around atomic operations.

Patterns
- Exclusive flow (claim before await):
```ts
// Bad: isCurrent() checked only after awaiting delivery; a second submission can win.
// Good: claim synchronously, then await.
async function resolveAskQuestion({ pending, deliverAttachments }) {
  const resolve = pending.resolve
  if (!resolve) return false
  pending.resolve = undefined; // claim immediately

  const hasAttachments = deliverAttachments && (pending.images?.length || pending.files?.length)
  if (hasAttachments) {
    await deliverAttachments(); // safe: second submission can’t resolve this ask now
  }
  resolve(pending.text ?? "");
  return true
}
```

- Per-session serialization for persistence ordering (teardown wins): chain writes per session key so overlapping “running” and “cancelled/teardown” don’t race.

- Capture the exact target now, update later (no searching by “latest”): when spawning background work after UI updates, store the target index/id immediately, then update that captured target when the async operation completes.

Adopt this as the default approach for: session-state persistence, UI attach/detach, pending-question resolution, checkpoint/hash updates, plugin generation lifetimes, and any async pipeline where late completions could overwrite newer state.