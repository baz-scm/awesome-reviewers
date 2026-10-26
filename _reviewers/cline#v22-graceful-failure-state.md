---
title: Graceful Failure State
description: 'Design failure paths as first-class flows: preserve user inputs, restore
  the last-known-good UI/config on rejected async work, keep user feedback consistent
  with the canonical action, and provide recovery or safe UI fallback.'
repository: cline/cline#v22
label: Error Handling
language: TSX
comments_count: 6
repository_stars: 70886
---

Design failure paths as first-class flows: preserve user inputs, restore the last-known-good UI/config on rejected async work, keep user feedback consistent with the canonical action, and provide recovery or safe UI fallback.

When an operation can fail (async actions, startup/transport requests, runtime restarts, or UI event sequences), require:
- **State restoration:** revert to `previous` mode/config and/or resync from the authoritative source (props/config/store) if the operation fails.
- **Input/draft preservation:** do not clear or mutate drafts/attachments/messages on failure.
- **Consistent messaging/constraints:** route alternate UI paths (e.g., suggestion tray actions) through the same validation + toast behavior as the canonical composer.
- **Recovery strategy:** failed startup should recover on the correct boundary (e.g., reconnect) rather than staying stuck.
- **Safe UI fallback + cleanup:** if the system enters a failure state, replace/unmount the stuck UI (avoid focus/pointer-event traps) and ensure teardown runs even when expected events (like pointerup) don’t fire.
- **Tests for failure:** add a test where the async operation rejects/times out and assert the state is restored and inputs remain.

Example pattern (restore-on-failure):
```ts
const previousMode = session.uiMode;
const newMode = previousMode === 'act' ? 'plan' : 'act';

session.toggleMode();
props.onModeChange(newMode).catch(() => {
  // restore last-known-good state
  session.setUiMode(previousMode);
  // optionally rely on resync from props/config rather than captured values
});
```

Apply the same principle to transport/startup gating (swap to a safe screen on later failure), and to user actions (only clear UI fields after the promise resolves successfully).