---
title: Stable Mount Visibility
description: When an app is gated by async readiness (hub connected/ready, auth, data
  bootstrap), prefer keeping the main app mounted and switching visibility to preserve
  user state—BUT gate side-effects so hide/show doesn’t re-run one-time initialization.
  Also, when failure occurs, replace (don’t cover) the app UI if any mounted dialogs/popovers
  could keep focus traps...
repository: cline/CLINE
label: React
language: TSX
comments_count: 4
repository_stars: 70839
---

When an app is gated by async readiness (hub connected/ready, auth, data bootstrap), prefer keeping the main app mounted and switching visibility to preserve user state—BUT gate side-effects so hide/show doesn’t re-run one-time initialization. Also, when failure occurs, replace (don’t cover) the app UI if any mounted dialogs/popovers could keep focus traps or disable body pointer events.

Apply this pattern:
- **Preserve state:** keep `<App />` mounted; hide it via a visibility controller (e.g., an `Activity`-like component) instead of unmounting.
- **Failure safety:** if the “startup failed” screen should own focus/pointer events, **replace** the app with the failure screen (so only one focus-managing UI is mounted).
- **One-time bootstrap vs reconnect refresh:** move “initial navigation/bootstrap” into a hook guarded by a `ref` so it runs only after the first successful initialization; still refresh derived state on every reconnect.
- **Test lifecycle transitions:** add coverage for `visible → hidden → visible` and for “failed first load → successful later load”.
- **Effect hygiene:** assume StrictMode can replay effects; ensure observers/dom work are created/destroyed predictably.

Example sketch:
```tsx
function useRemoteEnvironmentBootstrap() {
  const hasBootstrappedRef = useRef(false);

  useEffect(() => {
    if (!initializationSucceeded) return;

    // Always refresh active environment on load/reconnect.
    dispatch({ type: "refresh-active-environment" });

    // Only run initial navigation once.
    if (!hasBootstrappedRef.current) {
      hasBootstrappedRef.current = true;
      dispatch({ type: "select-environment-draft", payload: { draftId } });
    }
  }, [initializationSucceeded, dispatch, draftId]);
}

export function Home({ hubStatus }) {
  const [loaded, setLoaded] = useState(false);
  const hubReady = hubStatus === "ready";
  const hubFailed = hubStatus === "failed";

  useEffect(() => {
    if (hubReady) setLoaded(true);
  }, [hubReady]);

  const showApp = loaded && !hubFailed;

  return (
    <>
      {showApp ? (
        <Activity mode={hubReady ? "visible" : "hidden"}>
          <App />
        </Activity>
      ) : (
        <HubStartupScreen />
      )}
    </>
  );
}
```

This standard reduces focus/pointer bugs, preserves user context across transient connectivity, and prevents incorrect “re-navigation” on every hide/show cycle.