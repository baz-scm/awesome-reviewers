---
title: Manage hidden lifecycle
description: 'When you keep components mounted but toggle visibility (e.g., an <Activity>
  “hidden/visible” mode), treat that toggle as a lifecycle boundary: state may persist,
  but effects/DOM interactions (dialogs, focus traps, pointer-events) must behave
  as if the UI is inactive.'
repository: cline/cline#v30
label: React
language: TSX
comments_count: 4
repository_stars: 70894
---

When you keep components mounted but toggle visibility (e.g., an <Activity> “hidden/visible” mode), treat that toggle as a lifecycle boundary: state may persist, but effects/DOM interactions (dialogs, focus traps, pointer-events) must behave as if the UI is inactive.

Apply these rules:
1) Define persistence vs re-run behavior
- Persist user state that should survive recovery (selected conversation/session).
- Re-run data-fetching/refresh on reconnect.
- Do NOT re-run one-time “bootstrap navigation” on every hide/show.

2) Gate one-time initialization with refs
- Use a ref (that survives hidden/visible) to ensure initial navigation/dispatch happens only once after the first successful initialization.

3) Ensure cleanup/reset on hide
- If hiding mid-process (recording, streaming, listening), cancel the process and reset UI flags so showing again restores the correct interactive state.

4) Verify focus and pointer behavior
- Hidden UI should release focus traps and disable body pointer-events while startup/overlay is shown (especially with portaled dialogs).

Example pattern (gated bootstrap + visibility boundary):

```tsx
function useRemoteEnvironmentBootstrap({initializedOk, onBootstrap, onRefresh}) {
  const didBootstrapRef = useRef(false);

  useEffect(() => {
    if (!initializedOk) return;

    onRefresh(); // safe to run on every show/reconnect

    if (!didBootstrapRef.current) {
      didBootstrapRef.current = true;
      onBootstrap(); // one-time navigation/selection
    }
  }, [initializedOk, onBootstrap, onRefresh]);
}

// Usage with a visibility boundary (hidden/visible)
function Home({hubReady}) {
  const showApp = hubReady;
  return (
    <Activity mode={showApp ? "visible" : "hidden"}>
      <App />
    </Activity>
  );
}
```

5) Add tests for hide/show transitions
- Include scenarios like: hide during an active workflow, then show again; and reconnect sequences where effects might otherwise re-trigger incorrect navigation/selection.