---
title: Outcome-Driven Recovery UI
description: 'When handling async operations and startup/connectivity failures, make
  UI state transitions outcome-driven and provide explicit recovery paths.


  Apply these rules:'
repository: cline/cline?x=1
label: Error Handling
language: TSX
comments_count: 4
repository_stars: 70861
---

When handling async operations and startup/connectivity failures, make UI state transitions outcome-driven and provide explicit recovery paths.

Apply these rules:
1) Only mutate/clear user-visible state on success
- If an action can fail, keep the input/error visible so users can retry.

2) Tie recovery to the correct retry boundary
- For sidecar/transport-dependent lookups, rerun when transport becomes connected (or when the reconnect event fires), instead of assuming a one-time startup attempt will succeed.

3) Route the UI deterministically on failure
- During critical startup (Hub/sidecar), mount the main app only when ready; if it later fails again, switch back to a dedicated startup/failure screen.
- Prefer “replace” semantics over layered covering that can leave multiple control shells mounted.

4) Defensively clean up interactive state
- Ensure event handlers restore listeners/body styles even when expected events don’t fire (e.g., pointerup outside the window).

Example patterns:

```ts
// 1) Outcome-driven action state (don’t clear message on failure)
const commit = useCallback(async () => {
  if (!canCommit) return;
  const ok = await onAction({ type: "commit", message: message.trim(), push });
  if (ok) setMessage(""); // clear only on success
}, [canCommit, message, onAction, push]);

// 2) Retry boundary tied to transport/connect
useEffect(() => {
  if (transport !== "connected") return;
  desktopClient.invoke<string>("get_base_url")
    .then(setBaseUrl)
    .catch(() => undefined);
}, [transport]);

// 3) Deterministic failure routing
return loaded ? (
  <div inert={hubFailed}><App /></div>
) : (
  <HubStartupScreen {...startup} />
);
```

These practices prevent lost user input, ensure failures recover without manual refresh, and avoid inconsistent UI/control states during retries.