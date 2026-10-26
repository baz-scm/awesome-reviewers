---
title: Guard effects on resume
description: 'When UI visibility depends on external app state (e.g., hub readiness)
  or mode transitions (hide/show, reconnect, StrictMode replays), treat rendering
  and side-effects as separate concerns:'
repository: cline/cline#v25
label: React
language: TSX
comments_count: 4
repository_stars: 70891
---

When UI visibility depends on external app state (e.g., hub readiness) or mode transitions (hide/show, reconnect, StrictMode replays), treat rendering and side-effects as separate concerns:

1) Don’t just visually “cover” interactive UI if it can trap focus or keep pointer events enabled. Prefer replacing the subtree with a dedicated startup/empty state, or use a hiding mechanism that actually disables interaction and releases focus.
2) If you preserve state by keeping components mounted but hidden, assume React may re-run effects when the component becomes visible again. Make “bootstrap once” logic deterministic with refs/guards so reconnects refresh data without re-triggering initial navigation/selection.
3) For global listeners (keyboard/mouse/shortcut handlers) introduced by components, ensure critical flows suspend or guard competing handlers; stop propagation so unrelated capture/bubbling listeners don’t react during the critical interaction.

Example pattern (hide instead of unmount + bootstrap-once guard):

```tsx
function Home() {
  const startup = useHubStartup();
  const hubReady = startup.transport === "connected" && startup.hub.state === "ready";
  const [loaded, setLoaded] = useState(false);
  useEffect(() => {
    if (hubReady) setLoaded(true);
  }, [hubReady]);

  // Keep App mounted to preserve UI state, but disable interactivity while hub is down.
  return (
    <>
      {loaded ? (
        <Activity mode={hubReady ? "visible" : "hidden"}>
          <App />
        </Activity>
      ) : (
        <HubStartupScreen {...startup} />
      )}
    </>
  );
}

function useRemoteEnvironmentBootstrap() {
  const didBootstrapRef = useRef(false);

  useEffect(() => {
    if (!/* successful init */) return;

    // Always refresh active environment.
    // Only bootstrap navigation/selection once.
    if (!didBootstrapRef.current) {
      didBootstrapRef.current = true;
      dispatch(selectInitialDraft());
    }
  }, [/* dependencies */]);
}
```

Adopt this standard for any React code that toggles visibility, depends on async readiness, or uses global event handlers: make interactivity/focus behavior explicit, and make effect behavior correct across resume/reconnect.