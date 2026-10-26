---
title: Hide, Don’t Unmount
description: When you need to temporarily suspend a React UI (e.g., backend/Hub not
  ready, modal focus traps, in-progress recording/streaming), prefer keeping the component
  mounted and switching visibility instead of unmounting/remounting. This preserves
  state (like open conversations) while the hidden DOM can release focus traps and
  body pointer-events. Also ensure any...
repository: cline/cline#v6
label: React
language: TSX
comments_count: 2
repository_stars: 70864
---

When you need to temporarily suspend a React UI (e.g., backend/Hub not ready, modal focus traps, in-progress recording/streaming), prefer keeping the component mounted and switching visibility instead of unmounting/remounting. This preserves state (like open conversations) while the hidden DOM can release focus traps and body pointer-events. Also ensure any in-progress work or UI flags are properly canceled/reset when the UI becomes hidden, so showing it again restores the expected controls/behavior.

Pattern:
- Mount the app once when it’s safe the first time (e.g., first time the Hub is truly `ready`).
- When not ready later, keep the app mounted but render it in a hidden/disabled visibility mode (e.g., `<Activity mode="hidden">`).
- Add a “hide mid-process then show again” test to verify cancellation/reset and correct UI state.

Example:
```tsx
function Home() {
  const startup = useHubStartup();
  const hubReady =
    startup.transport === "connected" && startup.hub.state === "ready";

  const [loaded, setLoaded] = useState(false);
  useEffect(() => {
    if (hubReady) setLoaded(true);
  }, [hubReady]);

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
```

If you hide mid-operation (recording/streaming/composing), ensure your hide/visibility transition also reconciles internal state (cancel recording, reset flags) so the UI is consistent when it becomes visible again.