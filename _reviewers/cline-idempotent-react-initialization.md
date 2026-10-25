---
title: Idempotent React Initialization
description: Ensure React components that are shown/hidden or re-initialized during
  async reconnects preserve user state while preventing unintended re-bootstrapping.
repository: CLINE/cline
label: React
language: TSX
comments_count: 2
repository_stars: 70839
---

Ensure React components that are shown/hidden or re-initialized during async reconnects preserve user state while preventing unintended re-bootstrapping.

Apply this when:
- You keep components mounted but hidden (e.g., via an Activity-like container).
- Network/transport reconnects cause hooks/effects to rerun.

Coding standards:
1) Preserve state across hide/show, but deactivate side effects while hidden.
- Prefer a show/hide approach that preserves critical UI state (open conversation/selection) while stopping side-effect work and releasing UI constraints (portaled dialogs/popovers focus traps, body pointer-events).

2) Make initialization effects idempotent and split “first-time navigation/selection” from “subsequent refresh”.
- Use refs/guards so “initial navigation/bootstrap” runs only once after the first successful initialization.
- Allow refresh logic to run on every reconnect, but prevent it from re-dispatching navigation that would change the active selection.
- Do not count failed/cancelled loads as “initialized”.

3) Test the exact hide/show + reconnect behavior.
- Add coverage that toggles visibility (visible → hidden → visible) and asserts the active thread/selection remains stable, while refresh still occurs as expected.

Example pattern (mimics the discussed approach):

```tsx
function Home() {
  const startup = useHubStartup();
  const hubReady = startup.transport === "connected" && startup.hub.state === "ready";

  // Mount once hub is first ready; hide afterward to preserve state.
  const [loaded, setLoaded] = useState(false);
  useEffect(() => {
    if (hubReady) setLoaded(true);
  }, [hubReady]);

  return loaded ? (
    <Activity mode={hubReady ? "visible" : "hidden"}>
      <App />
    </Activity>
  ) : (
    <HubStartupScreen {...startup} />
  );
}

function App() {
  const initializedRef = useRef(false);

  useEffect(() => {
    // refresh logic can run every load/reconnect
    refreshRemoteEnvironment();

    // bootstrap/navigation only once after first successful initialization
    if (initializedRef.current) return;
    if (!startupIsSuccessfullyInitialized()) return;

    initializedRef.current = true;
    dispatchSelectEnvironmentDraft();
  }, [/* reconnect/loaded signals */]);

  return null;
}
```

If you follow these rules, hidden UI won’t steal focus or block interactions, and reconnects won’t accidentally change the user’s current conversation/selection via repeated bootstrapping.