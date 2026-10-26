---
title: Confirmed Success Recovery
description: When handling errors or recovery paths, never assume an operation “failed”
  (or “succeeded”) unless you can confirm it. Make cleanup, UI state changes, and
  restoration decisions conditional on confirmed outcomes, and treat “uncertain delivery”
  as a first-class state.
repository: cline/cline#v10
label: Error Handling
language: TSX
comments_count: 5
repository_stars: 70869
---

When handling errors or recovery paths, never assume an operation “failed” (or “succeeded”) unless you can confirm it. Make cleanup, UI state changes, and restoration decisions conditional on confirmed outcomes, and treat “uncertain delivery” as a first-class state.

Apply this standard:
- Gate irreversible actions on confirmed success: only detach sessions, clear user inputs, or finalize handoffs after the async result explicitly indicates success.
- Restore deterministically on UI/edge-case failures: if the expected counterpart event may never fire, add guards so the interaction ends and side effects (listeners, cursor/styles) are reverted based on observed state.
- Retry external-dependent initialization on reconnect/transport changes: timeouts should not require a full restart when a sidecar/service can reconnect.
- For “restore after send failure” flows: do not automatically restore persisted drafts unless you can guarantee the message/payload was not dispatched. If delivery might have partially occurred, degrade safely (e.g., suppress auto-restore, require explicit user review).

Example pattern (success-gated state mutation):
```ts
async function commitFlow(onAction: () => Promise<boolean>, message: string) {
  const ok = await onAction();
  if (!ok) return; // keep message/draft for user correction
  // only clear after confirmed success
  return message.trim();
}
```

This prevents “cleanup on failure” bugs, avoids resurrecting stale/incorrect user content after uncertain delivery, and improves resilience to both network/transport failures and UI event-stream edge cases.