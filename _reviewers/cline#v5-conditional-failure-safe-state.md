---
title: Conditional failure-safe state
description: 'When handling failures (async operations, startup dependencies, or unusual
  event sequences), ensure your code preserves invariants: only apply irreversible
  state changes/teardowns after success, keep user-visible inputs stable on failure,
  and provide an explicit retry/fallback path when the underlying dependency recovers.'
repository: cline/cline#v5
label: Error Handling
language: TSX
comments_count: 5
repository_stars: 70864
---

When handling failures (async operations, startup dependencies, or unusual event sequences), ensure your code preserves invariants: only apply irreversible state changes/teardowns after success, keep user-visible inputs stable on failure, and provide an explicit retry/fallback path when the underlying dependency recovers.

Apply this standard:
- Gate irreversible side effects (detach/clear/reset/close) behind confirmed success. If the operation fails, keep the prior state/resources attached.
- Model startup as a state machine: render a fallback when the required service is not ready or has failed, and avoid double-mounting or conflicting UI controls. After initial success, keep the app mounted and only switch to fallback on subsequent failures.
- Re-run failed initialization/lookups on reconnect/transport state changes. Treat reconnection as the retry boundary.
- Ensure graceful cleanup for event-driven flows: if an expected “end” signal (e.g., pointerup) is missed, end the interaction when the next event indicates the terminal condition (e.g., button no longer held), restoring styles/listeners.

Example pattern (success-gated state):
```ts
async function onCommitClicked() {
  // Attempt action returns success/failure.
  const ok = await onAction({ type: "commit", message });
  if (!ok) {
    // Preserve message/input; do not clear or detach.
    return;
  }
  // Only now clear UI state.
  setMessage("");
}
```

Example pattern (retry on reconnection):
```ts
useEffect(() => {
  if (transport !== "connected") return;
  desktopClient
    .invoke<string>("get_app_base_url")
    .then(setBaseUrl)
    .catch(() => {
      // Let a future reconnect trigger the retry.
    });
}, [transport]);
```

This reduces inconsistent UI/resources after failures and improves resilience via explicit recovery paths.