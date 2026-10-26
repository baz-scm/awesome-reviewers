---
title: Async Ownership Invariants
description: 'When multiple async tasks can touch the same logical state (session
  status, pending prompts, checkpoints, plugin runs, subprocess lifecycle), enforce
  these invariants:'
repository: cline/cline#v15
label: Concurrency
language: TypeScript
comments_count: 9
repository_stars: 70877
---

When multiple async tasks can touch the same logical state (session status, pending prompts, checkpoints, plugin runs, subprocess lifecycle), enforce these invariants:

1) Claim ownership before any await
- If you’re going to resolve/fulfill a shared promise or state, mark it claimed synchronously, then await delivery/side-effects.
- This prevents replacement messages from resolving the same item during an async gap.

```ts
async function resolvePendingAskQuestionSafe(opts: {
  prompt?: string;
  images?: string[];
  files?: string[];
  deliverAttachments?: (claimed: () => boolean) => Promise<void>;
}) {
  const resolve = pendingAskResolve;
  if (!resolve) return false;

  // Claim immediately: after this, replacements route elsewhere.
  pendingAskResolve = undefined;
  const claimed = () => /* check token or closure equality */ true;

  const hasAttachments = (opts.images?.length ?? 0) + (opts.files?.length ?? 0) > 0;
  if (hasAttachments && opts.deliverAttachments) {
    try {
      await opts.deliverAttachments(claimed);
      // If core echoes user input, avoid double-echo when attachments were delivered.
    } catch {
      // Fail delivery by falling back to text resolution (don’t leave run stuck).
    }
  }

  resolve(opts.prompt ?? "");
  return true;
}
```

2) Serialize shared writes (or make them order-safe)
- If two async operations can write the same record/field, chain them per logical key (per session, per runId) or use generation/version checks so the “latest wins” is deterministic.
- Guard terminal-state transitions so late/upcoming writes can’t overwrite cancelled/aborted/completed.

3) Capture per-attempt context, don’t use mutable “current”
- For retries/stop/rebuild: capture the target buffer/contexts at the start of the attempt.
- Orphan completions must not write into the currently active run’s state.

4) Bound all waits; fail safely when ownership disappears
- Any “pending request” that depends on another component must have deadlines/timeouts and a policy for special human-approval flows.

5) Clean up on settle; don’t leak resources across async boundaries
- Ensure timeouts/listeners/pipes/timers are cleared when a promise resolves or a fallback settles.
- Don’t accidentally pass abort signals that should not cancel singleton/critical sections (e.g., startup lock lifetimes).

Review heuristic: Ask “What happens if the earlier operation resolves after the later one started (or after cancellation/stop/teardown)?” If the answer isn’t explicitly handled by claim/serialization/generation checks plus bounded waits and cleanup, require a fix.