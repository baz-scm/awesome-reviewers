---
title: Graceful Failure Recovery
description: 'When an external dependency can fail (startup, sidecar/transport, user
  interaction events), design explicit recovery paths and fail-safe UI/state cleanup:'
repository: cline/cline#x
label: Error Handling
language: TSX
comments_count: 3
repository_stars: 70861
---

When an external dependency can fail (startup, sidecar/transport, user interaction events), design explicit recovery paths and fail-safe UI/state cleanup:

- Retry on the right lifecycle boundary: if a startup/request can time out, re-run the lookup on transport reconnect (not only on initial mount), and add a test that validates failure → reconnect → recovery.
- Replace, don’t “cover,” on failure: if the app can only be safely mounted when the hub is ready, then on later hub startup failure unmount/replace the app with the appropriate startup/failure screen to avoid focus/pointer/event traps.
- Assume abnormal termination can happen: for event-driven flows, include termination conditions that restore listeners/styles even when expected events (e.g., pointerup) don’t fire.

Example pattern (reconnect-driven retry + failure gate):
```ts
useEffect(() => {
  if (startup.transport === "connected") {
    desktopClient
      .invoke<string>("get_cline_app_base_url")
      .then(setClineAppBaseUrl)
      .catch(() => undefined);
  }
}, [startup.transport]);

const hubReady = startup.transport === "connected" && startup.hub.state === "ready";
const hubFailed = startup.transport === "connected" && startup.hub.state === "failed";

return (
  <>
    {hubReady ? <App /> : null}
    {(!hubReady || hubFailed) ? <HubStartupScreen {...startup} /> : null}
    {/* keep independent dialogs always mounted if they must overlay */}
  </>
);
```

Apply this anytime you manage asynchronous startup, external connections, or UI that must not remain mounted after failure.