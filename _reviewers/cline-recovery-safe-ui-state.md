---
title: Recovery-Safe UI State
description: 'When an async dependency (cloud restore, sidecar/Hub transport, source-control
  action) can fail or be retried, design UI and side effects so the app remains in
  a safe, recoverable state:'
repository: CLINE/cline
label: Error Handling
language: TSX
comments_count: 4
repository_stars: 70839
---

When an async dependency (cloud restore, sidecar/Hub transport, source-control action) can fail or be retried, design UI and side effects so the app remains in a safe, recoverable state:

- **Advance state only after success.** Don’t clear user-visible state, detach shared resources, or finalize transitions until the operation resolves successfully.
- **Provide explicit fallback for critical startup failures.** If a core service fails, render a dedicated startup/failure screen and **replace** the app UI instead of overlay-covering it (prevents focus/pointer-event traps and other “half-functional” UX).
- **Retry on the correct recovery trigger.** For environment/config lookups tied to transport, retry when the transport/connectivity state changes (e.g., reconnect), rather than relying on user refresh.

Example pattern (success-gated state + recoverable fallback):
```ts
const [loaded, setLoaded] = useState(false);
const hubFailed = transport === 'connected' && hub.state === 'failed';

// Only “commit” UI state when action succeeds
async function onCommit() {
  const ok = await onAction({ type: 'commit', message });
  if (!ok) return; // keep message + UI unchanged
  setMessage('');
}

// Failure-mode: replace app with fallback screen
return (
  <>
    {loaded && !hubFailed ? <App /> : null}
    {(!loaded || hubFailed) ? <HubStartupScreen /> : null}
  </>
);
```

Apply this as a standard for any feature that depends on external services: define the “safe state” on failure, ensure transitions/cleanup are success-gated, and wire retries to the most reliable recovery signal (typically reconnect).