---
title: Error-state success gating
description: 'When an operation can fail (async actions, restore/resume flows, hub/sidecar
  startup), handle failure paths explicitly:


  - **Gate dependent state changes on success.** Only detach/clear/advance UI state
  after the awaited operation succeeds.'
repository: cline/cline#v11
label: Error Handling
language: TSX
comments_count: 4
repository_stars: 70871
---

When an operation can fail (async actions, restore/resume flows, hub/sidecar startup), handle failure paths explicitly:

- **Gate dependent state changes on success.** Only detach/clear/advance UI state after the awaited operation succeeds.
- **Keep a consistent fallback on failure.** If you can’t complete the transition, leave the user in a recoverable state (don’t detach prematurely; don’t clear user input on rejected actions).
- **Retry on the real recovery signal.** Re-run failed startup lookups when the transport/hub becomes available again, rather than assuming the first attempt will recover.
- **Don’t overlay broken UI.** If readiness fails after the app mounted, **replace** the mounted view with the failure/startup screen to avoid focus/pointer traps.
- **Ensure cleanup/teardown is correct.** For transient UI interactions, restore listeners/styles when the interaction ends unexpectedly.

Example pattern (success-gated transition):

```ts
async function onResume(sessionId: string) {
  // Fail-safe: don’t detach cloud until local restore succeeds.
  try {
    const result = await restoreLocal(sessionId);
    detachCloud();
    return result;
  } catch (e) {
    // Keep consistent state so the user can retry.
    throw e;
  }
}

async function onCommit(message: string) {
  try {
    await commitToGit({ message: message.trim() });
    setMessage(""); // only clear after success
  } catch {
    // Leave message intact for retry.
  }
}
```

Apply this checklist during review: identify every awaited step that drives state/UI transitions, verify success vs failure behavior, confirm recovery (retry trigger), and confirm teardown/mount behavior during repeated failure events.