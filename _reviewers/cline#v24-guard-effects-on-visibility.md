---
title: Guard effects on visibility
description: 'When a React UI is shown/hidden in response to async startup/connection
  state (or visibility components like `<Activity>`), treat it as a lifecycle boundary:
  avoid losing user selection/state, prevent focus-trap regressions, and ensure side
  effects don’t re-run incorrectly.'
repository: cline/cline#v24
label: React
language: TSX
comments_count: 2
repository_stars: 70891
---

When a React UI is shown/hidden in response to async startup/connection state (or visibility components like `<Activity>`), treat it as a lifecycle boundary: avoid losing user selection/state, prevent focus-trap regressions, and ensure side effects don’t re-run incorrectly.

Standards:
1) Preserve app state across transient connection changes
- Prefer keeping key components mounted and only switching visibility (or using an Activity-like component) during “not ready / restarting” states.
- This preserves local UI state (e.g., open conversation selection) while you can still suppress UI interactions/DOM-driven focus issues.

2) Make side effects explicit: one-time bootstrap vs repeat refresh
- If hiding/showing causes effects to re-run, gate “navigation/bootstrap” actions so they run only once after the first successful initialization.
- Allow idempotent refresh logic (e.g., updating active environment) to run on every reconnect/visible cycle.

3) Regression-test the transition sequence
- Add tests that reproduce the visibility cycle: visible → hidden → visible across reconnect/initialization, with an open remote conversation selected.

Example pattern (one-time bootstrap after first success):
```tsx
function useRemoteEnvironmentBootstrap({ ready, activeRemoteEnvironment, dispatch, navigate }) {
  const bootstrappedRef = React.useRef(false);

  React.useEffect(() => {
    if (!ready) return;

    // Always refresh environment state on each successful load.
    // (Put any safe, repeatable updates here.)
    dispatch({ type: 'refresh-active-remote-environment', payload: activeRemoteEnvironment });

    // Only bootstrap navigation/selection once.
    if (!bootstrappedRef.current) {
      bootstrappedRef.current = true;
      dispatch({ type: 'select-environment-draft', payload: { environmentId: activeRemoteEnvironment.id } });
      navigate('/somewhere');
    }
  }, [ready, activeRemoteEnvironment, dispatch, navigate]);
}
```

How to apply:
- If your component depends on connection/startup state, review effects for assumptions that “visibility changes shouldn’t trigger selection-changing dispatches.”
- When you need “run once after first success,” use a `ref` guard (or equivalent state machine logic) rather than relying on mount timing.
- Ensure the hidden state releases any DOM/focus trapping (e.g., portaled dialogs, pointer-events) by keeping the UI architecture compatible with your visibility mechanism.