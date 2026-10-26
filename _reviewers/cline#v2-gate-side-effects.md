---
title: Gate side effects
description: 'When rendering React UI based on async/external readiness (or visibility
  toggles), treat lifecycle boundaries as first-class: preserve intentional UI state,
  prevent unintended re-initialization, and ensure cleanup restores interaction correctness.'
repository: cline/cline#v2
label: React
language: TSX
comments_count: 5
repository_stars: 70861
---

When rendering React UI based on async/external readiness (or visibility toggles), treat lifecycle boundaries as first-class: preserve intentional UI state, prevent unintended re-initialization, and ensure cleanup restores interaction correctness.

Practical rules:
- Choose mount vs hide deliberately:
  - If you must preserve state (e.g., selected conversation), keep the component mounted and use a visibility mechanism (e.g., `Activity`/`hidden` patterns) rather than unmounting.
  - If a failure mode can leave modals/dialogs/focus traps mounted, replace the tree (don’t merely cover it) so focus/pointer-event state can’t persist.
- Separate “one-time initialization” from “reconnect refresh”:
  - Effects triggered by visibility/mount changes often rerun; guard one-time actions with a `useRef` “first success” marker.
  - Still allow refresh logic to run after reconnect, but avoid changing the user’s current selection/thread unexpectedly.
- Ensure cleanup and state restoration on hide/unmount:
  - If a hidden/unmounted view cancels in-progress work (recording, streaming, etc.), reset the UI flags so when it becomes visible again it returns to the correct state.
- Model user intent vs programmatic intent explicitly:
  - For scroll/pin/focus logic, track “targets you initiated” in refs so emitted events don’t get mistaken for user actions.
  - Add event-target checks so keyboard/mouse handlers don’t trigger when the user is interacting with focused child controls.

Example (one-time bootstrap guarded by first successful readiness):
```tsx
function useRemoteEnvironmentBootstrap(/* deps */) {
  const didBootstrapRef = React.useRef(false);

  React.useEffect(() => {
    let cancelled = false;

    async function run() {
      const ok = await initializeRemote(/* ... */);
      if (cancelled) return;

      // Always refresh derived data on reconnect...
      refreshActiveEnvironment();

      // ...but only do navigation/selection bootstrap once.
      if (!didBootstrapRef.current && ok) {
        didBootstrapRef.current = true;
        dispatch(selectEnvironmentDraft(/* ... */));
        navigate(/* ... */);
      }
    }

    run();
    return () => {
      cancelled = true;
    };
  }, [/* reconnect/reload signals */]);
}
```

Applying this standard will prevent common React UX regressions: focus traps after async failures, lost selections due to effect reruns, stale UI flags after cancellation, and incorrect “user intent” detection for interactions like scrolling or keyboard navigation.