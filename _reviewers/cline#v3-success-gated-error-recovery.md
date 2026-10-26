---
title: Success-Gated Error Recovery
description: 'When handling failures in async/UI flows, treat success as a prerequisite
  for irreversible state changes and for restoring persisted content. In practice:'
repository: cline/cline#v3
label: Error Handling
language: TSX
comments_count: 6
repository_stars: 70863
---

When handling failures in async/UI flows, treat success as a prerequisite for irreversible state changes and for restoring persisted content. In practice:

- Success-gate mutations: only detach/advance/clear when the operation result confirms success; on failure, keep the prior state attached/preserved.
- Preserve user intent on failure: if an action (e.g., commit/send) fails, keep drafts/messages so the user can retry without retyping.
- Be uncertainty-aware for restoration: don’t automatically restore cached user content when delivery/side effects are uncertain—restore only for “definitely undispatched” cases, otherwise fall back to a safe UI state and/or require user confirmation.
- Recover on reconnect/restart: re-run idempotent startup lookups when transport state changes (e.g., after sidecar reconnect) and swap to a dedicated fallback UI when startup fails.
- Fail-safe cleanup: ensure listeners/styles/resources are restored even when expected events don’t fire (e.g., missing pointerup).

Example (success-gated commit message):
```ts
const commit = useCallback(async (push: boolean) => {
  if (!canCommit) return;
  try {
    const ok = await onAction({ type: "commit", message: message.trim(), push });
    if (ok) setMessage(""); // clear only on confirmed success
  } catch {
    // keep message for retry
  }
}, [canCommit, message, onAction]);
```

Apply the same pattern to session detach/restore and composer restoration: only perform “detach”/“restore” after verified outcomes; otherwise keep the safer state (attached cloud session, preserved draft, or fallback startup screen).