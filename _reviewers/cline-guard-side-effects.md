---
title: Guard side effects
description: In React, any effect that listens to global/input events or performs
  one-time navigation/initialization must be explicitly coordinated with UI lifecycle
  and state ownership.
repository: CLINE/CLINE
label: React
language: TSX
comments_count: 5
repository_stars: 70837
---

In React, any effect that listens to global/input events or performs one-time navigation/initialization must be explicitly coordinated with UI lifecycle and state ownership.

Apply this standard:
- **Gate side effects with explicit conditions**: before acting on keydown/keyup/scroll/focus, check the relevant “permission/state” (e.g., shortcuts suspended, hub ready, pinned ownership).
- **Use deterministic lifecycle boundaries**: if you must preserve UI state, prefer **hide** (keep mounted) over **unmount**, but ensure hidden content releases focus traps and blocks pointer events (e.g., via an `Activity`/visibility mechanism).
- **Make bootstrapping idempotent**: run “initial navigation/bootstrap” only once after the first successful readiness; subsequent reconnects should refresh data without re-triggering initial navigation that would change selection.
- **Respect event ownership and input source**: for complex interactions (scroll, pinned state), distinguish user-driven events from programmatic ones and ignore inputs that originate from focused child controls.
- **Prevent unintended propagation**: when a component owns a key interaction, stop it from reaching other handlers.

Example pattern (one-time bootstrap + event gating):
```tsx
function useOneTimeBootstrap({ isReady }: { isReady: boolean }) {
  const didBootstrapRef = useRef(false);

  useEffect(() => {
    if (!isReady || didBootstrapRef.current) return;
    didBootstrapRef.current = true;

    // initial, selection-preserving navigation
    dispatch(selectEnvironmentDraft());
  }, [isReady]);
}

function onKeyDownOwned(event: KeyboardEvent, { isSuspended }: { isSuspended: boolean }) {
  if (isSuspended) return;
  if (!matchesOwnedAccelerator(event)) return;

  event.preventDefault();
  event.stopImmediatePropagation();
  performOwnedAction();
}
```