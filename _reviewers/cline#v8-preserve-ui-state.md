---
title: Preserve UI State
description: 'When React UI transitions between “startup/loading/hidden/recovered”
  states, treat it like a state machine: preserve user state, avoid accidental effect
  reruns, and make event handling deterministic.'
repository: cline/cline#v8
label: React
language: TSX
comments_count: 5
repository_stars: 70867
---

When React UI transitions between “startup/loading/hidden/recovered” states, treat it like a state machine: preserve user state, avoid accidental effect reruns, and make event handling deterministic.

**Standards**
- **Prefer “mount once, toggle visibility” for recoverable screens** so conversation selection, drafts, and open dialogs aren’t lost and focus traps don’t get stuck. (Hidden UI should release pointer-events/focus traps; visible UI should take over cleanly.)
- **Make one-time initialization idempotent**: any “bootstrap navigation” should run only after the first successful initialization, while subsequent reconnects may refresh data but must not re-trigger one-time selection/navigation.
- **Persist state across show/hide** using `useRef` (not component remount) and guard effects with “first successful” refs.
- **Differentiate user input vs programmatic actions** for scroll/navigation: track programmatic targets separately so user scroll logic doesn’t misinterpret programmatic updates.
- **Guard event handlers by focus/target** so key/mouse interactions intended for child controls don’t trigger parent behavior.
- **Use semantic interactive elements** (`button` for click/keyboard activation); avoid anchors for actions unless you implement full keyboard semantics.

**Example pattern (bootstrap once, preserve selection across visibility toggles)**
```tsx
function useRemoteEnvironmentBootstrap({ status, dispatch, selectDraft }) {
  const bootstrappedRef = React.useRef(false);

  React.useEffect(() => {
    if (status !== "ready") return;

    // Always refresh active environment on reconnect
    dispatch({ type: "refresh_active_remote_environment" });

    // But only bootstrap navigation/selection once
    if (!bootstrappedRef.current) {
      bootstrappedRef.current = true;
      selectDraft();
    }
  }, [status, dispatch, selectDraft]);
}
```

**What to test**
- Open a conversation, trigger the hide/show or loading recovery, and assert the same conversation remains selected.
- Verify reconnect doesn’t re-run one-time navigation.
- Add interaction tests for scroll/pinning behavior and for keyboard events when focus is inside child controls.

Adopting this set of rules prevents common React UI regressions: state loss on show/hide, accidental focus trapping, and incorrect interaction handling after reconnects or programmatic updates.