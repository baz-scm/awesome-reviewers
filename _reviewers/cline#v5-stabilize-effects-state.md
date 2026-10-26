---
title: Stabilize effects & state
description: 'When UI visibility changes (e.g., startup gating, modal/Activity visible↔hidden),
  treat lifecycle as part of your state contract: keep components mounted when you
  must preserve user state, and explicitly control which effects should run only once
  vs on every reconnect/input.'
repository: cline/cline#v5
label: React
language: TSX
comments_count: 4
repository_stars: 70864
---

When UI visibility changes (e.g., startup gating, modal/Activity visible↔hidden), treat lifecycle as part of your state contract: keep components mounted when you must preserve user state, and explicitly control which effects should run only once vs on every reconnect/input.

Apply these rules:
- Prefer “mount once + hide” for flows where state must persist (selected conversation/session, draft selection). Avoid unmount/remount unless you truly want state loss.
- If visibility toggling causes effect re-runs, split concerns:
  - Run one-time bootstraps only after the first successful initialization.
  - Still refresh derived state on later reconnects.
  - Implement the “run once” boundary with a ref/flag that survives visibility hiding.
- Scope input handlers so they only respond to the intended origin/target:
  - Ignore key presses originating from focused child controls.
  - Distinguish user vs programmatic updates so scroll/unpin logic doesn’t misfire.
  - Prevent event leakage when a keybinding should not reach nested editors.

Example (one-time bootstrap after first successful init):
```ts
function useRemoteEnvironmentBootstrap(/* deps */) {
  const didBootstrapRef = useRef(false);

  useEffect(() => {
    if (!initSucceeded) return;

    // Always refresh what must stay current
    refreshActiveRemoteEnvironment();

    // But only run initial navigation/selection once
    if (!didBootstrapRef.current) {
      didBootstrapRef.current = true;
      dispatch(selectEnvironmentDraft({ threadId: initialThreadId }));
    }
  }, [initSucceeded, /* refresh deps */]);
}
```

Practical checklist:
- If user state must survive visibility changes, verify the component is not unmounted.
- Audit effects for implicit “runs on every visibility change” behavior; add a one-time ref/guard where needed.
- For key/scroll handlers, add target checks and internal “origin” tracking (user vs programmatic) before updating state.