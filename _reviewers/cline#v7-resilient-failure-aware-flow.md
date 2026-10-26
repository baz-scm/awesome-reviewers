---
title: Resilient Failure-Aware Flow
description: 'Implement explicit, failure-aware control flow: (1) model “ready vs
  failed vs loading” states, (2) retry/repair on lifecycle changes (e.g., reconnect),
  (3) gate cleanup/detach actions on successful completion, and (4) provide a graceful
  UI fallback when the system can’t reach the ready state. In event-driven code, don’t
  rely on perfect event...'
repository: cline/cline#v7
label: Error Handling
language: TSX
comments_count: 4
repository_stars: 70865
---

Implement explicit, failure-aware control flow: (1) model “ready vs failed vs loading” states, (2) retry/repair on lifecycle changes (e.g., reconnect), (3) gate cleanup/detach actions on successful completion, and (4) provide a graceful UI fallback when the system can’t reach the ready state. In event-driven code, don’t rely on perfect event delivery—terminate interactions using invariants when “expected” events (like pointerup) never arrive.

Practical checklist:
- **Success-gated cleanup:** Only detach/cleanup resources after the dependent operation succeeds; on failure, leave the state intact so recovery is possible.
- **Reconnect-driven retry:** For startup/network/sidecar calls, re-run lookup/recovery when transport state transitions (e.g., “connected” after reconnect) rather than only once.
- **Failure UI fallback:** Render a dedicated fallback/recovery screen when startup fails; avoid double-mounting controls—mount the shell consistently and swap only the app/content as needed.
- **Event robustness:** Add defensive termination conditions (e.g., check pointer button state) so interactions end safely even if the environment misses expected events.

Example (success-gated detach + reconnect-driven retry + fallback UI):
```ts
function AppRoot() {
  const startup = useHubStartup();
  const hubReady = startup.transport === "connected" && startup.hub.state === "ready";
  const hubFailed = startup.transport === "connected" && startup.hub.state === "failed";

  // Retry/repair logic example (pseudo): re-run the lookup whenever connected
  // rather than only once.
  useEffect(() => {
    if (startup.transport !== "connected") return;
    desktopClient.invoke("get_app_url")
      .then(setAppUrl)
      .catch(() => {
        // leave unresolved; will retry on next connected transition
      });
  }, [startup.transport]);

  // Success-gated cleanup example (pseudo): detach only after restore succeeds
  const resume = async (sessionId: string) => {
    const ok = await restoreLocalSession(sessionId);
    if (ok) detachCloudSession();
    // on failure, keep cloud session attached for recovery
  };

  if (!hubReady || hubFailed) return <HubStartupScreen {...startup} />;
  return <div className="contents">{/** App */}</div>;
}
```