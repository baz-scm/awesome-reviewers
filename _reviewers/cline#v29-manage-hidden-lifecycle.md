---
title: Manage hidden lifecycle
description: 'When React components transition between “visible” and “hidden” (without
  a full unmount), treat lifecycle like a real state machine: preserve intended UI
  state, but explicitly control side effects, focus/pointer behavior, and any in-progress
  work.'
repository: cline/cline#v29
label: React
language: TSX
comments_count: 5
repository_stars: 70893
---

When React components transition between “visible” and “hidden” (without a full unmount), treat lifecycle like a real state machine: preserve intended UI state, but explicitly control side effects, focus/pointer behavior, and any in-progress work.

Apply these rules:
1) Prefer a “hide, don’t unmount” pattern only when you truly want state retention. Ensure hidden mode also releases focus traps/pointer-events and hides/removes portaled dialogs/popovers.
2) Split effects into:
   - one-time bootstrap (e.g., initial navigation/selection): run only after the first successful initialization; guard with a `ref` so show/hide or reconnect doesn’t re-trigger it.
   - per-reconnect refresh (e.g., environment data): allow it to run every time the dependency changes.
3) Make hide/show mid-interaction deterministic: if a user action can be in progress (recording/streaming/etc.), cancel it and reset UI flags when hidden, so the component returns to the correct inactive state when shown again.
4) During “input capture” phases, suspend competing global behavior and prevent other listeners from acting (e.g., keybinding/quit handlers) to avoid accidental actions.

Example (bootstrap once, refresh on reconnect; preserve selection across Activity hide/show):
```ts
function useRemoteEnvironmentBootstrap({ status, dispatch, select }) {
  const bootstrappedRef = useRef(false);

  useEffect(() => {
    if (status !== "ready") return;

    // Always refresh environment
    dispatch(select.refreshActiveRemoteEnvironment());

    // But bootstrap navigation only once
    if (!bootstrappedRef.current) {
      dispatch(select.initialNavigation());
      bootstrappedRef.current = true;
    }
  }, [status, dispatch, select]);
}
```

If you adopt a global listener capture (shortcut recording), also enforce a clear “suspended” gate that every competing handler checks before acting.