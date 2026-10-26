---
title: Failure-Aware Recovery Gates
description: 'When an operation or dependency can fail (including retries after reconnect),
  make UI and state transitions failure-aware: (1) don’t commit irreversible changes
  (detach, clear drafts, reset messages) until the async action succeeds; (2) when
  failures are transient (transport restart/reconnect), re-attempt the failed work
  when the dependency returns and...'
repository: cline/cline#v28
label: Error Handling
language: TSX
comments_count: 5
repository_stars: 70892
---

When an operation or dependency can fail (including retries after reconnect), make UI and state transitions failure-aware: (1) don’t commit irreversible changes (detach, clear drafts, reset messages) until the async action succeeds; (2) when failures are transient (transport restart/reconnect), re-attempt the failed work when the dependency returns and update the UI to the correct failure/success screen; and (3) ensure cleanup so interruption/edge-cases (e.g., missing pointerup) don’t leave stale listeners or inconsistent state.

Apply it like this:
- Success-gate state changes
  - Preserve prior state on failure so the user/dependency can retry.
  - Clear UI inputs only after the operation resolves successfully.
- Recover on reconnect/state transitions
  - Use the dependency’s “ready/failed/connected” signals as the retry boundary.
  - If the dependency transitions to failed after the app already mounted, swap out the interactive UI for a safe startup/failure UI (so focus/interaction doesn’t get trapped).
- Always clean up on unexpected interruption
  - Restore styles/listeners and end the interaction when the termination condition can’t be delivered (e.g., release outside window).

Minimal pattern examples:

// 1) Success-gate irreversible detaching
const [resetCloudSession, detachCloudSession] = cloud;
const resumeSession = useCallback(async (sessionId: string) => {
  // Keep remote attached until local resume succeeds.
  const ok = await propsOnResumeSession(sessionId);
  if (ok) detachCloudSession();
  return ok;
}, [propsOnResumeSession, detachCloudSession]);

// 2) Retry failed startup work on reconnect
useEffect(() => {
  if (transport !== "connected") return;
  desktopClient
    .invoke<string>("get_cline_app_base_url")
    .then(setClineAppBaseUrl)
    .catch(() => {
      // no-op; next connected/reconnect will retry
    });
}, [transport]);

// 3) Don’t clear UI on failure
async function onCommit() {
  try {
    await onAction({ type: "commit", message: message.trim(), push: false });
    setMessage(""); // only on success
  } catch {
    // keep message so user can retry
  }
}

// 4) Swap UI when dependency fails later
return (
  <>
    {hubReady ? <App /> : <HubStartupScreen {...startup} />}
    <HubUpdateRequiredDialog />
  </>
);

// 5) Ensure interaction cleanup
const handleMove = (e: PointerEvent) => {
  if (!e.buttons) {
    // restore cursor/styles + remove listeners
    endDrag();
    return;
  }
  updateHeightFromPointer(e);
};

This standard prevents “half-applied” failures (lost sessions, cleared user inputs, trapped UI) and ensures recovery is automatic when the underlying dependency becomes healthy again.