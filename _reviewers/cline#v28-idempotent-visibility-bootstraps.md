---
title: Idempotent visibility bootstraps
description: When components can be hidden/shown (e.g., `Activity` visible/hidden)
  or reconnected, ensure React side-effects don’t accidentally re-run “initialization”
  and mutate critical state.
repository: cline/cline#v28
label: React
language: TSX
comments_count: 4
repository_stars: 70893
---

When components can be hidden/shown (e.g., `Activity` visible/hidden) or reconnected, ensure React side-effects don’t accidentally re-run “initialization” and mutate critical state.

Apply this checklist:
- Prefer *hiding* over *unmounting* for recoverable UI so local state (open conversations, selected session) and focus behavior aren’t reset.
- Separate **bootstrap** from **refresh**:
  - Bootstrap work that must happen only once after the first successful init should be gated with a `useRef` (and only count successful/complete runs).
  - Refresh work that should run after reconnects should be allowed to run every time.
- Make visibility transitions deterministic:
  - If the component is hidden mid-process, cancel/cleanup the in-progress work and reset any UI flags so when it becomes visible again the UI is correct.
- Respect first-mount and intent boundaries:
  - Props like `initial*` should apply on first mount only.
  - Event handlers should guard against “programmatic” vs “user” changes and ignore inputs targeted at focused child controls.
- Add regression tests that explicitly toggle visibility and simulate reconnect/failure paths while asserting key state (e.g., active conversation/thread and correct UI mode).

Example (bootstrap once, refresh on every successful load):
```tsx
function useRemoteEnvironmentBootstrap(loadFn: () => Promise<{ ok: boolean }>, dispatch: any) {
  const didBootstrapRef = React.useRef(false);

  React.useEffect(() => {
    let cancelled = false;
    (async () => {
      const result = await loadFn();
      if (cancelled || !result.ok) return;

      // Refresh runs every time...
      dispatch({ type: 'set_active_remote_environment', payload: /*...*/ });

      // ...bootstrap only once.
      if (!didBootstrapRef.current) {
        didBootstrapRef.current = true;
        dispatch({ type: 'select-environment-draft', payload: /*...*/ });
      }
    })();

    return () => { cancelled = true; };
  }, [loadFn, dispatch]);
}
```

Use this standard to prevent subtle regressions where hiding/showing or reconnecting triggers effects that overwrite selection/navigation or leave the UI in an inconsistent state.