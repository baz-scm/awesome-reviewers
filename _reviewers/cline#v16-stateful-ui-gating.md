---
title: Stateful UI gating
description: When React UI depends on async/system readiness or modal flows, explicitly
  coordinate rendering *and* side effects so hidden/failed states don’t leave active
  focus traps, pointer-event blockers, or competing global handlers.
repository: cline/cline#v16
label: React
language: TSX
comments_count: 6
repository_stars: 70882
---

When React UI depends on async/system readiness or modal flows, explicitly coordinate rendering *and* side effects so hidden/failed states don’t leave active focus traps, pointer-event blockers, or competing global handlers.

Apply these rules:
1) Prefer “replace” over “cover” for failed/blocked states that could leave interactive dialogs mounted.
   - If the underlying app may still hold focus traps, swap it out for the startup/modal screen.
2) If you must preserve state, hide via a mechanism that disables effects and interaction (e.g., an Activity-like mode) rather than just CSS-hidden.
   - Ensure hidden mode truly tears down effects, including portaled dialogs/popovers.
3) Separate “initial bootstrap” from “reconnect refresh”.
   - On visibility changes or reconnects, refresh data/state, but avoid re-running navigation/selection side effects unless it’s the first successful initialization.
4) Guard global keyboard/shortcut handlers during modal/recording flows.
   - Use a suspension flag; both the recorder and any other handlers should check it.
   - Stop propagation (and prefer stopImmediatePropagation when appropriate) so other capture-phase listeners don’t also act.
5) Keep interactive UI keyboard/a11y and responsive.
   - Use correct roles/aria for non-standard controls (e.g., resize handles as separators with value semantics).
   - Constrain dialogs to viewport height with scrolling so actions stay reachable.

Example pattern (hide vs replace + idempotent bootstrap):
```tsx
function AppGate({ hubReady }: { hubReady: boolean }) {
  const [loaded, setLoaded] = useState(false);
  useEffect(() => { if (hubReady) setLoaded(true); }, [hubReady]);

  const firstBootstrapDone = useRef(false);
  useEffect(() => {
    if (!loaded) return;
    if (!hubReady) return; // refresh handled elsewhere if needed

    // Refresh always; bootstrap navigation only once
    refreshActiveEnvironment();
    if (!firstBootstrapDone.current) {
      dispatchSelectInitialDraft();
      firstBootstrapDone.current = true;
    }
  }, [loaded, hubReady]);

  // If you need to avoid focus traps on failure, replace:
  // return hubFailed ? <StartupScreen /> : <Activity mode={hubReady ? 'visible' : 'hidden'}>...</Activity>

  return loaded ? (
    <Activity mode={hubReady ? 'visible' : 'hidden'}>
      <App />
    </Activity>
  ) : (
    <StartupScreen />
  );
}
```
