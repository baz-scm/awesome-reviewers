---
title: Recover From Failures Gracefully
description: Implement error recovery and failure-safe cleanup by wiring state transitions
  to the *actual completion signal* and providing fallback behavior when expected
  events/requests fail.
repository: cline/cline#v29
label: Error Handling
language: TSX
comments_count: 3
repository_stars: 70893
---

Implement error recovery and failure-safe cleanup by wiring state transitions to the *actual completion signal* and providing fallback behavior when expected events/requests fail.

Practical rules:
1) Gate destructive cleanup on success
- If you must detach/commit/stop a process to prevent incorrect behavior, do it only after the dependent local restore succeeds; ensure failed operations leave the safer/consistent path running.

2) Retry on the real lifecycle boundary
- For bootstrapping/lookup calls that can fail or time out, don’t rely on “user refresh” as the retry point. Instead, re-run when the underlying system becomes healthy again (e.g., transport reconnect/connected state), and add a test for “first attempt fails, later reconnect succeeds.”

3) Add invariants/guards for event-driven flows
- When relying on UI events (like `pointerup`) that may not fire (release outside window), add a secondary termination condition based on state (e.g., “no button held”) and restore listeners/styles.

Example patterns (self-contained):

// 1) Gate cleanup on async success
async function resumeSession(sessionId: string) {
  // Don’t detach cloud until local restore succeeds.
  try {
    const result = await restoreLocalSession(sessionId);
    detachCloudSession(); // only after success
    return result;
  } catch (e) {
    // keep cloud attached / safe behavior on failure
    throw e;
  }
}

// 2) Retry lookup on reconnect/state change
useEffect(() => {
  if (!transport.isConnected) return;
  transport.invoke('get_base_url')
    .then(setBaseUrl)
    .catch(() => {
      // allow next connected-state transition to retry
    });
}, [transport.connectedState]);

// 3) Defensive drag termination
function startDrag() {
  const onMove = (e: PointerEvent) => {
    if (!e.buttons) {
      endDrag(); // restore body styles + remove listeners
      return;
    }
    // ...apply drag delta...
  };
  const endDrag = () => {
    document.body.style.cursor = '';
    window.removeEventListener('pointermove', onMove);
    // remove other listeners as needed
  };
  window.addEventListener('pointermove', onMove);
}
