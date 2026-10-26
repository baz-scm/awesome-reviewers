---
title: Success-Gated Error Recovery
description: 'When handling failures in async/interactive flows, treat “success vs
  failure” as a first-class state boundary. Concretely:


  1) Gate destructive side effects on success'
repository: cline/cline#v24
label: Error Handling
language: TSX
comments_count: 4
repository_stars: 70891
---

When handling failures in async/interactive flows, treat “success vs failure” as a first-class state boundary. Concretely:

1) Gate destructive side effects on success
- Do not detach, clear, close, or dispose shared resources until the operation that justifies it has succeeded.
- If the operation can fail and you’ll need to retry, keep the previous resource attached/available.

2) Define deterministic recovery triggers
- For startup/connection-dependent lookups, base retries on stable signals (e.g., transport reconnect) rather than ad-hoc refresh calls.
- Ensure the retry action is idempotent and won’t corrupt state if invoked multiple times.

3) Tie UI state changes to the actual result
- Avoid “optimistic” UI clears for operations that can fail.
- Prefer operations that return success/failure (or throw) and update UI only on success.

4) Provide graceful, failure-specific UI fallbacks
- On major failure modes, degrade the UI by replacing the app/view with an appropriate fallback (preserving window controls/layout), rather than layering multiple control surfaces.

Example pattern (success-gated detach + result-driven UI):

```ts
async function resume(sessionId: string) {
  try {
    // keep cloud attached until local restore truly succeeds
    const restored = await restoreLocal(sessionId);
    if (!restored) return; // cloud still attached
    detachCloudSession();
  } catch (e) {
    // failure: do nothing destructive; recovery can happen on next reconnect/resume
  }
}

async function onCommit() {
  const ok = await onAction({ type: "commit", message, push: true });
  if (ok) setMessage(""); // only clear on success
}
```

Adopt this as a review checklist: “What failure state exists?”, “What is the retry trigger?”, “Which side effects are allowed on failure?”, and “How does the UI reflect success vs failure?”