---
title: Rollback optimistic state on failure
description: 'When an async operation changes UI or session state, don''t let a rejected
  promise either crash the app or leave the system in an inconsistent state. Catch
  errors from async calls and decide deliberately how to handle each case:'
repository: cline/cline#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
label: Error Handling
language: TSX
comments_count: 3
repository_stars: 70965
---

When an async operation changes UI or session state, don't let a rejected promise either crash the app or leave the system in an inconsistent state. Catch errors from async calls and decide deliberately how to handle each case:

1. For state transitions driven by optimistic UI updates (e.g. toggling a mode, switching sessions), only commit irreversible side effects (detaching a connection, discarding previous data) after the async operation has confirmed success. If it fails, catch the error and restore the UI/state to its previous value instead of leaving a half-applied change.

```ts
const toggleMode = useCallback(() => {
	const previousMode = session.uiMode;
	const newMode = previousMode === "act" ? "plan" : "act";
	session.toggleMode(); // optimistic update
	props.onModeChange(newMode).catch((error: unknown) => {
		// restart failed; revert UI and config back to previous mode
		session.setUiMode(previousMode);
		applyInteractiveModeConfig(previousMode);
		showToast(error);
	});
}, [props, session]);
```

Similarly, destructive handoffs (e.g. detaching a cloud session before resuming locally) should happen only after the dependent async action succeeds, so a failure doesn't strand the user without either state.

2. For non-critical, fire-and-forget actions (e.g. opening an external link) where failure has no meaningful recovery path, it's acceptable to swallow the error with an empty `.catch(() => {})` purely to avoid an unhandled rejection — but this should be a conscious, documented choice, not a default pattern for all async failures.

Apply this standard by always asking: "what happens to the state/UI if this promise rejects?" and ensure failures either roll back cleanly or are explicitly and safely ignored.</description>
