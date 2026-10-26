---
title: Idempotent Mount and Hide
description: 'When React UI depends on async readiness (transport/session state) or
  special interaction modes, design around three rules:


  1) Preserve state intentionally (hide vs cover)'
repository: cline/cline#v15
label: React
language: TSX
comments_count: 6
repository_stars: 70877
---

When React UI depends on async readiness (transport/session state) or special interaction modes, design around three rules:

1) Preserve state intentionally (hide vs cover)
- If you need state continuity across connectivity failures/retries, keep the app mounted and switch visibility (e.g., an <Activity mode="hidden"> wrapper) instead of unmounting.
- Ensure hidden mode releases focus traps and disables pointer interactions, so dialogs/overlays don’t remain active behind the startup screen.

2) Make bootstrapping idempotent
- Any “run once” initialization that performs navigation or selection (e.g., bootstrapping a remote environment) must not re-run on every visibility toggle/reconnect.
- Use a ref/flag that survives hide/show to ensure the one-time navigation happens only after the first successful initialization, while allowing subsequent reconnects to refresh data.

3) Suspend competing side effects during special modes
- If a UI mode temporarily needs exclusive control (e.g., key recording, startup overlay, modal interaction), suspend global shortcuts/listeners for the duration and guard handlers with an is-suspended check.
- Also stop propagation strongly enough to prevent other capture/bubble listeners from reacting.

4) Keep critical UI reachable
- Cap dialogs/panels against viewport height and reflow on resize so follow-up actions remain clickable (especially on small windows).

Example pattern (mount-on-ready, hide when not ready, idempotent bootstrap):

```tsx
function Home() {
  const startup = useHubStartup();
  const hubReady = startup.transport === "connected" && startup.hub.state === "ready";
  const hubFailed = startup.transport === "connected" && startup.hub.state === "failed";

  const [loaded, setLoaded] = useState(false);
  useEffect(() => {
    if (hubReady) setLoaded(true);
  }, [hubReady]);

  // One-time bootstrap after first successful init
  const bootstrapDoneRef = useRef(false);
  useEffect(() => {
    if (!hubReady) return;
    if (!bootstrapDoneRef.current) {
      bootstrapDoneRef.current = true;
      // run initial navigation/selection here
    }
    // always refresh data on reconnect
    refreshActiveEnvironment();
  }, [hubReady]);

  return (
    <>
      {loaded ? (
        <Activity mode={hubReady && !hubFailed ? "visible" : "hidden"}>
          <App />
        </Activity>
      ) : null}
      {!loaded || hubFailed ? <HubStartupScreen {...startup} /> : null}
    </>
  );
}
```

Adopt this standard when reviewing React changes involving async state transitions, visibility toggles, focus/overlay behavior, keyboard/modal interactions, or reconnect recovery paths.