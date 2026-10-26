---
title: Graceful failure recovery
description: When something fails (action rejection, connectivity timeout, or runtime
  interaction edge case), code must (1) prevent invalid work by reusing the same guards
  used by the primary UI, (2) preserve user input/state when the operation doesn’t
  succeed, (3) recover automatically on transient infrastructure changes (e.g., reconnect/sidecar
  restart), and (4)...
repository: cline/cline#v4
label: Error Handling
language: TSX
comments_count: 6
repository_stars: 70864
---

When something fails (action rejection, connectivity timeout, or runtime interaction edge case), code must (1) prevent invalid work by reusing the same guards used by the primary UI, (2) preserve user input/state when the operation doesn’t succeed, (3) recover automatically on transient infrastructure changes (e.g., reconnect/sidecar restart), and (4) ensure the user can always interact with the correct surface (unmount/inert the failing surface rather than covering it with a focus/pointer trap).

Apply it as follows:
- Action + state: only mutate/clear user state after the async operation succeeds.
- Guard before side effects: run the same “can send” / validation checks before performing the action; blocked sends should show the same error/toast and leave drafts/attachments untouched.
- Retry on reconnect: key recovery effects off the transport’s connected state (so a timed-out startup lookup reruns after the sidecar reconnects).
- UI gating: on startup failure, replace the app with the recovery UI (or inert it) so focus/pointer behavior can’t get stuck.
- Interaction cleanup: handle cases where expected events don’t fire (e.g., release outside window) by ending the interaction when signals indicate the drag should stop, and always restore global styles/listeners.

Example (state cleared only on success):
```ts
const commit = useCallback(async () => {
  if (!canCommit) return;
  try {
    await onAction({ type: "commit", message: message.trim(), push });
    setMessage(""); // clear only after success
  } catch {
    // keep message so user can retry; toast handled by caller/host
  }
}, [canCommit, message, onAction]);
```

Example (recovery reruns on reconnect):
```ts
useEffect(() => {
  if (transport !== "connected") return;
  desktopClient
    .invoke("get_cline_app_base_url")
    .then(setUrl, () => undefined);
}, [transport]);
```

Example (avoid focus/pointer trap by replacing UI):
```tsx
return (
  <>
    {loaded ? <div className="contents" inert={hubFailed}><App /></div> : null}
    {(!loaded || hubFailed) ? <HubStartupScreen {...startup} /> : null}
  </>
);
```