---
title: Ready-state lifecycle safety
description: When implementing React UI that changes with external readiness (startup/connected/failed),
  explicitly manage what stays mounted and make lifecycle side-effects safe across
  hidden/show or StrictMode replays.
repository: cline/cline?x=1
label: React
language: TSX
comments_count: 4
repository_stars: 70861
---

When implementing React UI that changes with external readiness (startup/connected/failed), explicitly manage what stays mounted and make lifecycle side-effects safe across hidden/show or StrictMode replays.

**Standards**
1. **Failure vs. unready:**
   - If the previous UI can contain dialogs/popovers that trap focus or disable pointer events, **replace** the tree with the failure/startup screen (don’t just cover it).
   - If you need to preserve user context (selected conversation, draft state), **hide** the app while the system is unready, ensuring hidden DOM tears down effects/portals and releases focus/pointer behavior.

2. **Effect idempotency across visibility:**
   - If hiding/showing causes effects to re-run, separate:
     - **One-time bootstrap** (e.g., initial navigation/selection) guarded by a `ref` that survives hide/show.
     - **Repeatable refresh** (e.g., environment/state refresh) that can run on every reconnect.

3. **Cleanup & timing assumptions:**
   - Ensure observers/timers are cleaned up.
   - If using external stores, don’t rely on “first effect” ordering under StrictMode; re-check store state if needed.

**Pattern (one-time bootstrap guarded by ref)**
```ts
function useRemoteEnvironmentBootstrap(/* deps */) {
  const bootstrappedRef = useRef(false);

  useEffect(() => {
    let cancelled = false;

    async function run() {
      const ok = await initRemoteEnvironment();
      if (!ok || cancelled) return;

      // One-time navigation/selection
      if (!bootstrappedRef.current) {
        bootstrappedRef.current = true;
        dispatch(selectEnvironmentDraft(/* ... */));
        navigate(/* ... */);
      }

      // Always refresh current active environment
      refreshActiveRemoteEnvironment();
    }

    run();
    return () => {
      cancelled = true;
    };
  }, [/* reconnect inputs */]);
}
```

Applying these rules prevents focus/pointer regressions and avoids state/selection bugs caused by effect re-execution during readiness transitions.