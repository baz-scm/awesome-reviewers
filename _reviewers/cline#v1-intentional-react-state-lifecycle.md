---
title: Intentional React State Lifecycle
description: 'React components should encode clear ownership and intentional lifecycle
  behavior: keep context minimal, control mount vs hide/show deliberately, gate one-time
  side effects after successful readiness, and model user-vs-programmatic event intent—while
  honoring user preferences for motion.'
repository: cline/cline#v1
label: React
language: TSX
comments_count: 7
repository_stars: 70862
---

React components should encode clear ownership and intentional lifecycle behavior: keep context minimal, control mount vs hide/show deliberately, gate one-time side effects after successful readiness, and model user-vs-programmatic event intent—while honoring user preferences for motion.

Apply this standard:
- Context/state ownership
  - Put only truly shared, stable/owned values into context. Derive per-view links/data locally instead of syncing derived values through context.
- Mount vs hide/show
  - If you must preserve component state across temporary “not ready” phases, prefer keeping the component mounted and using a visibility/hide mechanism that also releases focus/pointer traps.
  - If a failure must change window controls/overlays, replace the UI instead of stacking overlays that can duplicate controls or trap focus.
- Gate initialization side effects
  - When reconnects/resumes occur, prevent repeated “bootstrap” dispatches/navigation from re-running. Use refs to track whether the one-time initialization succeeded and completed.
- Event-driven UI semantics
  - For scroll/gesture-heavy UIs, track “intent” (e.g., pinned/unpinned) with refs, and distinguish user actions from programmatic ones to avoid misinterpreting scroll events.
- Accessibility preferences
  - Any motion/scroll behavior must respect `prefers-reduced-motion` unless an explicit prop overrides it.

Example pattern (mount once + hide/show + one-time bootstrap gating):
```tsx
function Home() {
  const startup = useHubStartup();
  const hubReady = startup.transport === "connected" && startup.hub.state === "ready";
  const hubFailed = startup.transport === "connected" && startup.hub.state === "failed";

  const [loaded, setLoaded] = React.useState(false);
  React.useEffect(() => {
    if (hubReady) setLoaded(true);
  }, [hubReady]);

  const didBootstrapRef = React.useRef(false);

  React.useEffect(() => {
    if (!hubReady) return;
    if (!didBootstrapRef.current) {
      didBootstrapRef.current = true;
      // run one-time successful initialization (dispatch/select/navigation)
    }
    // on reconnect: refresh owned data, but don’t re-run one-time selection
  }, [hubReady]);

  return (
    <>
      {loaded ? (
        <Activity mode={hubReady ? "visible" : "hidden"}>
          <App />
        </Activity>
      ) : null}
      {!loaded || hubFailed ? <HubStartupScreen {...startup} /> : null}
    </>
  );
}
```

Use this checklist to review PRs in React: “Is the state stored in the right place?”, “What happens on reconnect/failure?”, “Do effects re-run and unintentionally change selection/focus?”, “Are event semantics modeled correctly with refs?”, and “Does the UI respect reduced-motion and other accessibility preferences?”