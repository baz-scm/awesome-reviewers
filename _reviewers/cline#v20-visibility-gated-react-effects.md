---
title: Visibility gated React effects
description: When UI behavior depends on an external system being “ready”, structure
  React components so you preserve user/application state without re-triggering one-time
  navigation/selection side effects.
repository: cline/cline#v20
label: React
language: TSX
comments_count: 4
repository_stars: 70886
---

When UI behavior depends on an external system being “ready”, structure React components so you preserve user/application state without re-triggering one-time navigation/selection side effects.

Standard:
1) Gate initial mount on first successful readiness. Don’t render interactive app UI until the required dependency (e.g., Hub) is ready.
2) After the first successful mount, prefer keeping the app mounted and switching visibility (hide/show) rather than unmounting/remounting, so conversations/selection state remain intact.
3) Ensure hidden UI fully releases focus and interaction locks (focus traps, portaled dialogs, body `pointer-events`) while the startup/overlay screen is shown.
4) Treat reconnects carefully: hiding/showing may cause effects to rerun. Split logic into:
   - One-time bootstrap actions (guard with a `useRef`/state flag so they only run after the first successful initialization).
   - Repeating “refresh” actions (safe on every reconnect/visible transition).
5) Add tests that cover visible → hidden → visible across reconnection/recovery with an open remote conversation (assert the active thread/selection doesn’t change unexpectedly).
6) For interactive controls involved in these UI states (e.g., resize handles), use correct semantics and keyboard/ARIA behavior (`role=separator`, `tabIndex`, `aria-valuenow`, Arrow key support, etc.).

Example pattern (one-time bootstrap + refresh, while visibility toggles):

```tsx
function useRemoteEnvironmentBootstrap({ dispatch, loadState }) {
  const didBootstrapRef = React.useRef(false);

  React.useEffect(() => {
    if (!loadState.success) return;

    // Always refresh on reconnect
    dispatch({ type: 'activeRemoteEnvironment/refresh', payload: loadState.env });

    // Only do navigation/selection once after the first successful initialization
    if (!didBootstrapRef.current) {
      didBootstrapRef.current = true;
      dispatch({ type: 'select-environment-draft', payload: loadState.initialDraftId });
    }
  }, [dispatch, loadState.success, loadState.env, loadState.initialDraftId]);
}

// In the page/component:
// - Mount once hubReady first becomes true
// - Keep <App/> mounted, but wrap it with an Activity-like visibility switch
//   so state is preserved and focus/pointer-events are released when hidden.
```

Apply this standard whenever component lifecycle is coupled to external readiness, reconnection, or overlay transitions—especially on desktop/web hybrid UIs where focus management and effect reruns can break user selection or trap dialogs.