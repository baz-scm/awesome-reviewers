---
title: Recover and Gate Failures
description: 'Adopt deterministic failure recovery patterns: (1) retry only from the
  correct boundary (often reconnect/transport state), (2) perform irreversible side
  effects only after the success path completes, and (3) gate or unmount UI/event
  resources on failure so the app can’t get stuck (focus traps, stale handlers, detached
  elements).'
repository: cline/cline#v23
label: Error Handling
language: TSX
comments_count: 5
repository_stars: 70889
---

Adopt deterministic failure recovery patterns: (1) retry only from the correct boundary (often reconnect/transport state), (2) perform irreversible side effects only after the success path completes, and (3) gate or unmount UI/event resources on failure so the app can’t get stuck (focus traps, stale handlers, detached elements).

Practical checklist
- Choose a retry trigger: if a request depends on environment/transport, re-run it on transport “connected”/reconnect, not on unrelated state (and add a test that fails once then succeeds after reconnect).
- Success-gate destructive transitions: when a “detach/replace/clear” happens, ensure it occurs after the operation that depends on it succeeds; on failure, keep the old behavior attached.
- Always clean up on aborted interactions: assume “end” events may not fire (pointerup outside window, aborted resume, etc.); add fallback termination and restore styles/listeners.
- Gate UI mounting by failure state: don’t cover/mask the main app on startup failure if that can trap focus or disable pointer events—replace/unmount instead, and keep critical dialogs above via z-index.

Example patterns (success-gated side effects + retry on boundary)
```ts
// 1) Retry on the right boundary (e.g., reconnect)
useEffect(() => {
  if (transportState !== "connected") return;
  let cancelled = false;
  desktopClient
    .invoke<string>("get_cline_app_base_url")
    .then((url) => {
      if (!cancelled) setClineAppBaseUrl(url);
    })
    .catch(() => {
      // keep current state; recovery will happen on next reconnect
    });
  return () => { cancelled = true; };
}, [transportState]);

// 2) Only detach/clear after success
async function resume(sessionId: string) {
  // don’t detach yet
  const restoreOk = await restoreLocalSession(sessionId);
  if (!restoreOk) return; // keep cloud attached
  detachCloudSession();
}

// 3) Gate rendering on failure to avoid “stuck” UI
return startup.failed
  ? <HubStartupScreen {...startup} />
  : <App />;
```

This reduces fragile failure paths, prevents inconsistent UI/state after errors, and makes recovery testable.