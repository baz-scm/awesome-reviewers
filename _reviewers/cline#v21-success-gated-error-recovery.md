---
title: Success-gated error recovery
description: 'When operations can fail (async resume/commit/startup/interaction),
  treat related UI/session state as transactional: only perform irreversible changes
  after success, ensure deterministic cleanup on failure/edge interactions, and add
  explicit recovery paths tied to reconnect/state changes.'
repository: cline/cline#v21
label: Error Handling
language: TSX
comments_count: 5
repository_stars: 70886
---

When operations can fail (async resume/commit/startup/interaction), treat related UI/session state as transactional: only perform irreversible changes after success, ensure deterministic cleanup on failure/edge interactions, and add explicit recovery paths tied to reconnect/state changes.

Apply this standard:
- Success-gate irreversible updates: detach sessions, clear inputs, replace elements, and persist state only after the awaited action resolves successfully.
- Deterministic cleanup: if an interaction can end abnormally (e.g., pointer release outside the window), add a fallback condition to restore listeners and transient styles/state.
- Recover on state changes: if an initial request can fail, re-run it when the transport/session becomes “connected/ready” again; don’t rely on users refreshing or on stale single-shot effects.
- Failure-safe UI mounting: on startup failure, replace/unmount interactive components rather than merely covering them to avoid focus trapping and lingering pointer-event behavior.

Example pattern (success-gated mutation + recovery trigger):
```ts
// Success-gated irreversible update
async function resume(sessionId: string) {
  // keep remote attached until local resume succeeds
  const ok = await propsOnResumeSession(sessionId);
  if (!ok) return;           // no detach on failure
  detachCloudSession();
}

// Recovery re-run on reconnect/transport change
useEffect(() => {
  if (transport !== "connected") return;
  desktopClient
    .invoke<string>("get_cline_app_base_url")
    .then(setClineAppBaseUrl)
    .catch(() => undefined);
}, [transport]);
```

Checklist for PRs:
- What state changes are irreversible, and are they gated on success?
- What is the cleanup behavior for failure/edge outcomes (listeners/styles/resources)?
- If the first attempt fails, is there a retry/recovery hook tied to an observable state change?
- During failure UI, are interactive components replaced/unmounted to prevent focus/pointer-event issues?