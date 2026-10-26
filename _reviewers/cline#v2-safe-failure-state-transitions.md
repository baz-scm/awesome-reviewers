---
title: Safe Failure-State Transitions
description: 'Treat every async/edge-case failure as a distinct state transition:
  don’t irreversibly detach, clean up, or clear user-visible state until success is
  confirmed; and always provide a deterministic recovery path (retry signal or degraded
  UI).'
repository: cline/cline#v2
label: Error Handling
language: TSX
comments_count: 5
repository_stars: 70861
---

Treat every async/edge-case failure as a distinct state transition: don’t irreversibly detach, clean up, or clear user-visible state until success is confirmed; and always provide a deterministic recovery path (retry signal or degraded UI).

Apply this standard:
- **Commit state only on success:** If an action returns a promise, update/clear UI state (e.g., input text) only after it resolves successfully; on rejection, keep the user’s state so they can retry.
- **Delay irreversible side effects:** For operations that detach/replace external resources, ensure detachment/cleanup happens only after the “restore/replace” step succeeds; if the operation fails, leave the system in a safe/consistent state.
- **Recovery must be tied to a real signal:** Retry failed lookups or re-initialize only when the underlying transport/ready condition changes (e.g., reconnect/next “connected”/“ready”), not solely on initial mount.
- **Provide a degraded UI path:** If critical startup fails, replace (or clearly gate) the main app with a dedicated fallback screen so controls/drag regions remain correct and partially-initialized components aren’t left mounted.
- **Defend against missing events / undelivered signals:** Where OS/browser event delivery is unreliable, add guards that restore invariants (e.g., end a drag when a move happens without the button held).

Example pattern (commit clears only on success):
```ts
const commit = async () => {
  try {
    await onAction({ type: "commit", message: message.trim() });
    setMessage(""); // only after success
  } catch {
    // keep message so user can retry
  }
};
```