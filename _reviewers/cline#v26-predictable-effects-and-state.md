---
title: Predictable Effects And State
description: For React components with lifecycle-sensitive UI (visibility toggles,
  reconnect/retry flows, StrictMode, portaled dialogs, scroll/selection state), make
  state transitions predictable by separating one-time bootstrap from recurring refresh
  and by explicitly tracking event ownership.
repository: cline/cline#v26
label: React
language: TSX
comments_count: 4
repository_stars: 70893
---

For React components with lifecycle-sensitive UI (visibility toggles, reconnect/retry flows, StrictMode, portaled dialogs, scroll/selection state), make state transitions predictable by separating one-time bootstrap from recurring refresh and by explicitly tracking event ownership.

Apply these rules:
- Prefer “hide” over “unmount” when you need to preserve user state. Unmounting often re-triggers effects and can break selection, focus, and dialog behavior.
- Gate one-time initialization inside effects using a ref so it runs only after the first successful initialization (not every time visibility flips back to visible).
- Distinguish programmatic UI changes from user-driven ones (scrolling, focusing, navigation). Track programmatic targets so your event handlers don’t misinterpret those events as user intent.
- Be StrictMode-safe: don’t assume effects run only once; use refs to remember prior outcomes and re-check store state when effects may replay.
- Add tests covering the transition sequence (e.g., visible → hidden → visible, reconnect, failed-first-load then success).

Example pattern (one-time bootstrap + recurring refresh):
```ts
function useRemoteEnvironmentBootstrap({ isReady, dispatch, actions }) {
  const firstSuccessRef = React.useRef(false);

  React.useEffect(() => {
    if (!isReady) return;

    // Always refresh derived environment.
    actions.refreshActiveRemoteEnvironment();

    // Only bootstrap navigation/selection once.
    if (!firstSuccessRef.current) {
      firstSuccessRef.current = true;
      dispatch(actions.selectEnvironmentDraft({ /* ... */ }));
    }
  }, [isReady, dispatch, actions]);
}
```

If your UI includes scroll/selection “pinning” or other intent-sensitive behavior, enforce event ownership similarly (e.g., track an `ourScrollTarget` and ignore scroll events until the user meaningfully intervenes).