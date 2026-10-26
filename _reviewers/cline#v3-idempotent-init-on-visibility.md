---
title: Idempotent init on visibility
description: When UI is gated/hidden based on external readiness (e.g., Hub startup),
  treat “visible/hidden” transitions as lifecycle events that can re-trigger effects.
  Ensure side-effects are intentional, idempotent, and testable.
repository: cline/cline#v3
label: React
language: TSX
comments_count: 4
repository_stars: 70863
---

When UI is gated/hidden based on external readiness (e.g., Hub startup), treat “visible/hidden” transitions as lifecycle events that can re-trigger effects. Ensure side-effects are intentional, idempotent, and testable.

**Standard**
1. **Choose the right rendering strategy**
   - **Hard failure:** replace the app with the startup/failure screen so no app dialogs remain mounted.
   - **Soft not-ready:** prefer hiding (e.g., an `Activity`-style wrapper) to preserve user state while releasing focus traps/pointer-event behavior.
2. **Make initialization run-once (after success), not on every visibility toggle**
   - Guard “navigation/bootstrap/select” logic with a `ref` so it runs only once after the first successful initialization.
3. **Ensure cleanup restores UI state**
   - If a component can be active while hidden (recording/streaming), cleanup must both stop the operation **and** reset the UI state/flags so the next show is correct.
4. **Add regression tests**
   - Cover at least: `visible → hidden → visible` and “failed first load then success” so bootstrapping and selection remain stable.

**Pattern (run-once bootstrap after success)**
```tsx
function useRemoteEnvironmentBootstrap({ isReady, activeEnv, dispatch }) {
  const didBootstrapRef = React.useRef(false);

  React.useEffect(() => {
    if (!isReady) return;

    // Refresh any derived environment state every time,
    // but only run navigation/selection bootstrap once after the first success.
    if (!didBootstrapRef.current) {
      dispatch({ type: 'select-environment-draft', payload: { envId: activeEnv.id } });
      didBootstrapRef.current = true;
    }
  }, [isReady, activeEnv, dispatch]);
}
```

Applying this keeps focus/pointer behavior correct during readiness transitions, preserves user selection, and prevents hidden/show cycles from causing unintended navigation or UI regressions.