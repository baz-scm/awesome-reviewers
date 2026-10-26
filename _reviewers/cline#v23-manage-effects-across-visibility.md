---
title: Manage Effects Across Visibility
description: 'When React components change visibility (hidden vs unmounted, or temporary
  “startup/recording” modes), treat it as a lifecycle boundary: explicitly control
  (a) which effects may run, (b) which global listeners may react, and (c) whether
  hidden UI releases focus/pointer resources.'
repository: cline/cline#v23
label: React
language: TSX
comments_count: 3
repository_stars: 70889
---

When React components change visibility (hidden vs unmounted, or temporary “startup/recording” modes), treat it as a lifecycle boundary: explicitly control (a) which effects may run, (b) which global listeners may react, and (c) whether hidden UI releases focus/pointer resources.

Apply these rules:
1) Hide vs unmount deliberately
- If you must preserve state, keep the component mounted but ensure the hidden mode truly releases interaction ownership (focus traps, portaled dialogs/popovers, and body/pointer-events) so the visible screen is the only interactive layer.
- Gate re-appearance on authoritative readiness state (e.g., hub status “ready”) to avoid early retries.

2) Guard one-time initialization across hide/show
- Effects may re-run when Activity/visibility changes. Use a ref (or equivalent state) to ensure “initial navigation/bootstrap” runs only once after the first successful initialization, while allowing safe refresh work on later reconnects.

3) Suspend global handlers during transient input modes
- If the UI enters a special mode (e.g., shortcut recording), introduce a shared “suspension” flag and have every competing handler check it. Cancel any in-flight related state (e.g., quit-hold timers) and stop further propagation when needed.

Example patterns (self-contained):

One-time bootstrap guarded by ref (prevents navigation shifting on visibility resume)
```ts
function useRemoteEnvironmentBootstrap({ status, dispatch }) {
  const bootstrappedRef = useRef(false);

  useEffect(() => {
    if (status !== 'ready') return;

    // Always refresh environment, but only do initial navigation once.
    dispatch({ type: 'refresh-active-environment' });

    if (!bootstrappedRef.current) {
      bootstrappedRef.current = true;
      dispatch({ type: 'select-environment-draft' });
    }
  }, [status, dispatch]);
}
```

Global shortcut suspension during recording (prevents competing listeners)
```ts
const { suspendShortcuts, isShortcutsSuspended } = useShortcuts();

function ShortcutRecorder() {
  useEffect(() => {
    if (!recording) return;

    const release = suspendShortcuts(); // increments suspension counter
    const onKeyDown = (e: KeyboardEvent) => {
      e.preventDefault();
      e.stopImmediatePropagation(); // avoid other capture listeners
      // ...record key... 
    };
    window.addEventListener('keydown', onKeyDown, { capture: true });

    return () => {
      window.removeEventListener('keydown', onKeyDown, { capture: true });
      release(); // must be paired with suspend
    };
  }, [recording]);
}

function PageLevelShortcutListener({ onAction }) {
  useEffect(() => {
    const onKeyDown = (e: KeyboardEvent) => {
      if (isShortcutsSuspended()) return;
      onAction(e);
    };
    window.addEventListener('keydown', onKeyDown);
    return () => window.removeEventListener('keydown', onKeyDown);
  }, [onAction]);
}
```

Finally: add tests that explicitly cover transitions like visible→hidden→visible and success→failure→recovery so regressions (state drift, focus trapping, duplicated bootstrap, competing global handlers) are caught early.