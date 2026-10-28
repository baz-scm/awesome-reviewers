---
title: Hide stateful trees with Activity
description: When a large stateful subtree (e.g. the main app shell) must be temporarily
  taken off-screen during an async readiness transition (startup, reconnect, backend
  restart), prefer React's `Activity` (hidden/visible) over unmounting or covering
  it with an overlay. Unmounting discards state (open conversations, drafts, selections);
  covering it with an overlay...
repository: cline/cline?x
label: React
language: TSX
comments_count: 5
repository_stars: 70983
---

When a large stateful subtree (e.g. the main app shell) must be temporarily taken off-screen during an async readiness transition (startup, reconnect, backend restart), prefer React's `Activity` (hidden/visible) over unmounting or covering it with an overlay. Unmounting discards state (open conversations, drafts, selections); covering it with an overlay leaves effects running underneath, which can trap focus or keep `pointer-events` disabled on portaled dialogs. Hiding with `Activity` keeps component state alive while properly tearing down effects (closing dialogs/popovers, releasing focus traps, restoring body pointer-events) when hidden, and reruns them when shown again — so the previously open conversation/dialog state reappears correctly.

Two follow-up rules apply whenever you adopt this pattern:
1. Effects that should execute only once across the whole lifetime (e.g. one-time bootstrap/navigation on first successful load) must guard themselves with a `ref`, since `Activity` reruns effects on every show but refs survive hiding. Don't rely on the effect's dependency array alone to detect "first time."
2. Cleanup functions written for unmount must also reset any state that `Activity` preserves across hides (e.g. a mid-flight recording's `isListening`/`isProcessing` flags), otherwise the UI can resurface in a stale, inconsistent state when shown again.

Example shape:

```tsx
const [loaded, setLoaded] = useState(false);
useEffect(() => {
  if (ready) setLoaded(true);
}, [ready]);

return loaded ? (
  <Activity mode={ready ? "visible" : "hidden"}>
    <App />
  </Activity>
) : (
  <StartupScreen />
);

// Inside a bootstrap effect that must run only once:
const bootstrapped = useRef(false);
useEffect(() => {
  refreshEnvironment(); // safe to rerun every time shown
  if (bootstrapped.current) return;
  bootstrapped.current = true;
  dispatchInitialNavigation(); // only on first successful load
}, [environment]);

// Inside a recording/listening effect's cleanup:
useEffect(() => {
  startRecording();
  return () => {
    stopRecording();
    setIsListening(false); // reset state Activity would otherwise preserve
    setIsProcessing(false);
  };
}, []);
```