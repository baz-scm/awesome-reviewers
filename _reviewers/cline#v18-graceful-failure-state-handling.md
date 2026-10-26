---
title: Graceful failure-state handling
description: 'Treat failure/recovery as a first-class state in UI components: (1)
  make user-facing state changes conditional on success, (2) trigger recovery logic
  on reconnect/late failures, and (3) ensure interaction cleanup/termination paths
  even when expected events don’t fire.'
repository: cline/cline#v18
label: Error Handling
language: TSX
comments_count: 5
repository_stars: 70884
---

Treat failure/recovery as a first-class state in UI components: (1) make user-facing state changes conditional on success, (2) trigger recovery logic on reconnect/late failures, and (3) ensure interaction cleanup/termination paths even when expected events don’t fire.

How to apply
- Success-gate destructive/irreversible UI updates
  - Don’t clear forms, messages, or optimistic state unless the async action resolves successfully.
- Recover from external failures automatically
  - If a sidecar/hub/network request can fail at startup, rerun the lookup when the transport becomes connected again (or when the relevant state transitions back to a “retry point”).
- Replace (don’t cover) when switching app/system screens due to failure
  - If the main app must not remain mounted during startup failure, render a dedicated failure/startup screen instead of overlaying/covering the app—this prevents trapped focus and broken pointer/interaction handling.
- Add defensive termination + cleanup for user interactions
  - For drags/pointers, include a fallback to end the interaction and restore global styles/listeners when the button is no longer held—even if `pointerup` never arrives.

Example patterns
- Success-gated commit UI:
  ```ts
  const commit = useCallback(async () => {
    if (!canCommit) return;
    const ok = await onAction({ type: "commit", message: message.trim(), push });
    if (ok) setMessage("");
  }, [canCommit, message, onAction, push]);
  ```
- Reconnect-triggered recovery lookup:
  ```ts
  useEffect(() => {
    if (transport !== "connected") return;
    desktopClient
      .invoke<string>("get_cline_app_base_url")
      .then(setClineAppBaseUrl)
      .catch(() => undefined);
  }, [transport]);
  ```
- Replace gated UI on later hub failure:
  ```tsx
  const hubReady = transport === "connected" && hub.state === "ready";
  const hubFailed = transport === "connected" && hub.state === "failed";

  return (
    <>
      {hubReady && !hubFailed ? <App /> : null}
      {(!hubReady || hubFailed) ? <HubStartupScreen {...startup} /> : null}
    </>
  );
  ```

Outcome: fewer stale UI states after failures, safer interaction behavior, and predictable recovery without requiring a full reload.