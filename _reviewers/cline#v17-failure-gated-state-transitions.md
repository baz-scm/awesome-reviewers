---
title: Failure-gated state transitions
description: 'Treat failure as a first-class state: only perform irreversible state
  changes and UI state clearing after the operation is confirmed successful, and design
  recovery so the app can deterministically re-enter a valid state after failures
  or missed events.'
repository: cline/cline#v17
label: Error Handling
language: TSX
comments_count: 5
repository_stars: 70883
---

Treat failure as a first-class state: only perform irreversible state changes and UI state clearing after the operation is confirmed successful, and design recovery so the app can deterministically re-enter a valid state after failures or missed events.

Apply this as a checklist:
- **Gate side effects on success:** Defer detach/cleanup/mutations until the underlying async step reports success (or only after the local restore succeeds). If the step fails, keep the previous/safer state.
- **Make success explicit in APIs:** Have action functions resolve a **boolean** (or a typed result) so callers can update UI only on `true`.
- **Recover on reliable triggers:** If a startup request can fail (e.g., sidecar/transport), retry on the next dependable lifecycle event such as “transport connected/reconnected,” not only on initial mount.
- **Re-gate UI on critical startup failure:** When core subsystems fail, swap the mounted interactive surface (e.g., App ↔ startup screen) so you don’t keep focus/pointer behavior stuck in an invalid state; ensure higher-priority dialogs remain layered above.
- **Defensive cleanup for missed events:** When event systems can drop terminal signals (e.g., pointerup outside window), enforce invariants during the event stream (e.g., end drag when the pointer button is no longer held) and always restore global styles/listeners.

Example pattern (success boolean + failure-safe UI):
```ts
const commit = useCallback(async () => {
  // action returns success
  const ok = await onAction({ type: "commit", message: message.trim(), push: true });
  if (!ok) return;           // keep message / state on failure
  setMessage("");          // clear only after success
}, [onAction, message]);
```

Example pattern (defer irreversible cleanup):
```ts
const resume = useCallback(async (sessionId: string) => {
  // local resume may fail; don't detach cloud until it succeeds
  const ok = await propsOnResumeSession(sessionId);
  if (ok) detachCloudSession();
}, [propsOnResumeSession, detachCloudSession]);
```