---
title: Safe async state rollback
description: When a UI action triggers an async operation that can fail (switching
  modes, detaching a session, refreshing data), do not commit the dependent state
  change optimistically. Only apply the state transition after the async call resolves
  successfully, and on failure roll back using the current authoritative source of
  truth rather than a locally captured...
repository: cline/cline;
label: Error Handling
language: TSX
comments_count: 5
repository_stars: 70964
---

When a UI action triggers an async operation that can fail (switching modes, detaching a session, refreshing data), do not commit the dependent state change optimistically. Only apply the state transition after the async call resolves successfully, and on failure roll back using the current authoritative source of truth rather than a locally captured "previous" value, since multiple overlapping failures can make a stale snapshot inconsistent with reality. Additionally, never mask a failure by silently falling back to stale or placeholder data that could be read as a successful result, and never let a rejected/error state silently no-op in a way the user can't perceive — surface explicit, actionable feedback (e.g., a toast) when an action can't complete or isn't supported in the current state.

Example (mode toggle restart failure):
```ts
const toggleMode = useCallback(() => {
  const previousMode = session.uiMode;
  const newMode = previousMode === "act" ? "plan" : "act";
  session.toggleMode();
  props.onModeChange(newMode).catch((error: unknown) => {
    // Resync from the authoritative config, not the captured previousMode,
    // so repeated failures don't diverge from the real runtime state.
    session.setUiMode(props.config.mode);
    showToast(`Failed to switch mode: ${error}`);
  });
}, [props, session]);
```

Apply this pattern consistently: confirm success before finalizing a state transition (e.g., detach a cloud session only after a local resume succeeds), resync from source-of-truth state on rollback, hide/avoid rendering fallback data when the underlying fetch errored, and give users clear messaging when an action is rejected or unsupported instead of failing silently or acting on the wrong target.