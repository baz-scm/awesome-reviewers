---
title: Stateful error recovery
description: 'Ensure your code keeps user-facing state consistent and recoverable
  when failures or partial events occur.


  Apply these practices:

  1) Guard state transitions on success'
repository: cline/cline#v19
label: Error Handling
language: TSX
comments_count: 4
repository_stars: 70885
---

Ensure your code keeps user-facing state consistent and recoverable when failures or partial events occur.

Apply these practices:
1) Guard state transitions on success
- Don’t clear or mutate critical UI state unless the async operation succeeded.

2) Re-gate or retry on external readiness changes
- For sidecars/hubs/transports: mount or show fallback UIs based on readiness, and re-run lookups when the connection state changes so transient startup failures recover after reconnect.

3) Preserve invariants even when expected events don’t fire
- For pointer/DOM interactions: handle “missing event” scenarios by detecting alternative signals (e.g., button released) and always restore listeners/styles.

Example patterns:
- Commit UI: only clear message when the commit actually succeeded.

```ts
const commit = useCallback(async (push: boolean) => {
  if (!canCommit) return;
  try {
    await onAction({ type: "commit", message: message.trim(), push });
    setMessage(""); // clear only on success
  } catch {
    // keep message so the user can retry
  }
}, [canCommit, message, onAction]);
```

- External readiness gating + recovery:

```tsx
const startup = useHubStartup();
const hubReady = startup.transport === "connected" && startup.hub.state === "ready";
const hubFailed = startup.transport === "connected" && startup.hub.state === "failed";

return (
  <>
    {hubReady ? <App /> : null}
    {( !hubReady || hubFailed) ? <HubStartupScreen {...startup} /> : null}
  </>
);
```

Checklist:
- If an operation can fail, what user input/state might you accidentally discard?
- If an external system can reconnect/restart, do you re-run the relevant lookup/mount decision?
- If the environment can miss events (pointerup/blur), do you have a fallback to restore invariants (cleanup, styles, listeners)?