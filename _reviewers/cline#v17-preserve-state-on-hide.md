---
title: Preserve state on hide
description: 'When React components are temporarily hidden (e.g., startup overlays,
  Activity modes, drawers/panels), treat “visibility” as a first-class state transition:
  preserve user state, but prevent side effects (focus traps, dialogs, portaled UI,
  leaked events) from breaking correctness.'
repository: cline/cline#v17
label: React
language: TSX
comments_count: 4
repository_stars: 70883
---

When React components are temporarily hidden (e.g., startup overlays, Activity modes, drawers/panels), treat “visibility” as a first-class state transition: preserve user state, but prevent side effects (focus traps, dialogs, portaled UI, leaked events) from breaking correctness.

Apply these rules:
1) Prefer hiding over unmounting when state must survive
- Use a visibility mechanism (e.g., an <Activity mode="hidden"> wrapper) instead of conditionally removing the component, so conversation/selection/UI state persists.
- Ensure hidden state releases UI side effects (focus traps, pointer-events) via the visibility mechanism, not by unmounting.

2) Separate one-time bootstrap from reconnect/renewal logic
- Move “only once after first successful init” logic into a hook that uses a ref/flag so it doesn’t re-run after visibility toggles or reconnects.
- Still allow refresh logic to run on every reconnect where needed.

3) Explicitly model event ownership (user vs programmatic)
- For scroll: track whether a scroll was initiated programmatically and ignore/interpret resulting scroll events accordingly; only user input should un-pin.
- For keyboard: when handling a keybinding, stop propagation so the underlying UI (inputs/chat) doesn’t also process the keystroke.

Example pattern (visibility + one-time bootstrap + event ownership):

```ts
function useRemoteEnvironmentBootstrap(/* deps */) {
  const didBootstrapRef = useRef(false);

  useEffect(() => {
    if (!initialized) return;

    // Always refresh active environment on reconnect
    refreshActiveEnvironment();

    // Only run navigation/selection bootstrap once
    if (!didBootstrapRef.current) {
      didBootstrapRef.current = true;
      dispatch(selectEnvironmentDraft({ id }));
    }
  }, [initialized, /* reconnect deps */]);
}

function KeyboardHandler({ matches, onQuit }: { matches: (e: KeyboardEvent)=>boolean; onQuit: ()=>void }) {
  useEffect(() => {
    const onKeyDown = (e: KeyboardEvent) => {
      if (!matches(e)) return;
      e.preventDefault();
      e.stopImmediatePropagation(); // don’t let textarea/chat handle it
      onQuit();
    };
    window.addEventListener('keydown', onKeyDown);
    return () => window.removeEventListener('keydown', onKeyDown);
  }, [matches, onQuit]);
}
```

Result: consistent UI behavior across hub startup/recovery and remount/hide cycles, fewer focus/pointer-trap regressions, and correct state transitions for scroll and keyboard interactions.