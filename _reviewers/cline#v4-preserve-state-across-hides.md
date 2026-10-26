---
title: Preserve state across hides
description: 'When toggling complex React UIs (especially those with portals/focus
  traps), prefer *hiding* over unmounting, and make effects/reactivity intentional:'
repository: cline/cline#v4
label: React
language: TSX
comments_count: 4
repository_stars: 70864
---

When toggling complex React UIs (especially those with portals/focus traps), prefer *hiding* over unmounting, and make effects/reactivity intentional:

- **Keep state across visibility changes:** If you need to pause the UI while preserving open selections/state, mount once and switch between visible/hidden modes rather than unmounting.
- **Gate one-time bootstraps:** Split logic into “refresh” (runs on every reconnect) vs “initial navigation/bootstrap” (runs only after the first successful initialization). Use a `ref` to ensure one-time actions don’t replay when the component becomes visible again.
- **Separate user intent from programmatic updates:** For scroll, typing, resize, etc., track “who caused the change” via refs (e.g., `ourScrollTarget`) so programmatic updates don’t look like user actions.
- **Guard event handlers:** Only treat events as user intent when they originate from the intended target (e.g., don’t unpin on arrow keys aimed at focused child controls).

Example: one-time bootstrap after first successful load
```tsx
function useRemoteEnvironmentBootstrap(refreshDeps: unknown) {
  const didBootstrapRef = useRef(false);

  useEffect(() => {
    let cancelled = false;

    async function run() {
      const ok = await initializeRemoteEnvironment(refreshDeps);
      if (cancelled) return;

      // Refresh always updates current environment state.
      setActiveRemoteEnvironment(/* ... */);

      // Only the first *successful* load performs initial navigation.
      if (ok && !didBootstrapRef.current) {
        didBootstrapRef.current = true;
        dispatch(selectEnvironmentDraft(/* ... */));
      }
    }

    void run();
    return () => {
      cancelled = true;
    };
  }, [refreshDeps]);
}
```

And for interaction correctness (scroll pinning): track programmatic scroll targets and only change pinned state based on actual user input.

These practices prevent regressions where Activity hide/show, reconnections, or programmatic updates accidentally re-run initialization, drop selections, or misinterpret user intent.