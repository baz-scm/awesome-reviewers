---
title: Visibility-safe React gating
description: When gating an app on external readiness (hub startup, sidecar restarts,
  etc.), prefer *visibility* over unmounting and make effects/events aware of hidden
  vs visible states.
repository: cline/cline#v11
label: React
language: TSX
comments_count: 4
repository_stars: 70871
---

When gating an app on external readiness (hub startup, sidecar restarts, etc.), prefer *visibility* over unmounting and make effects/events aware of hidden vs visible states.

Apply these rules:
1) Keep stateful UI mounted when you need to preserve selections/conversations across recoveries. Hide it (e.g., with an `<Activity>`-style component or `inert`) rather than unmounting.
2) Ensure hidden content truly releases interaction: hidden UI should not keep focus traps or capture pointer events while the startup/overlay UI is shown.
3) Split effect logic into:
   - **One-time bootstrap** (run only after the first successful initialization).
   - **Reconnect refresh** (run on every successful reconnect), without re-dispatching actions that would change the active thread/environment.
   Use refs to track “first successful load” so hide/show doesn’t accidentally trigger bootstrap again.
4) During “modal-like” states (shortcut recording, startup screens), suspend/guard global handlers and stop event propagation so other window-level listeners don’t act on the same key events.
5) For custom interactive controls within gated views (drag/resize handles), implement accessibility + keyboard equivalents (proper role/ARIA and Arrow-key behavior).

Example pattern (bootstrap only once; refresh on reconnect; hide without unmount):

```tsx
function useRemoteEnvironmentBootstrap({ visible, envId, dispatch }) {
  const bootstrappedRef = React.useRef(false);

  React.useEffect(() => {
    if (!visible) return;
    // Always refresh on each successful load/reconnect.
    dispatch({ type: 'set_active_remote_environment', payload: envId });

    // But only run selection/bootstrap once.
    if (!bootstrappedRef.current) {
      bootstrappedRef.current = true;
      dispatch({ type: 'select-environment-draft' });
    }
  }, [visible, envId, dispatch]);
}

export default function Page() {
  const startup = useHubStartup();
  const hubReady = startup.transport === 'connected' && startup.hub.state === 'ready';

  return (
    <Activity mode={hubReady ? 'visible' : 'hidden'}>
      <App />
      {/* Startup/overlay UI rendered elsewhere when not ready */}
    </Activity>
  );
}
```

This combination prevents state loss, avoids focus/pointer leakage from hidden DOM (including effects like portals/popovers), and stops one-time initialization from re-running due to hide/show or reconnect timing.