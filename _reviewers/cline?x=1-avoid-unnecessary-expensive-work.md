---
title: Avoid Unnecessary Expensive Work
description: Before you add new async/IO/network work (or telemetry/UI reactions),
  verify whether the expensive data is already available, and constrain/guard the
  work so it only runs when necessary.
repository: cline/cline?x=1
label: Performance Optimization
language: TypeScript
comments_count: 6
repository_stars: 70861
---

Before you add new async/IO/network work (or telemetry/UI reactions), verify whether the expensive data is already available, and constrain/guard the work so it only runs when necessary.

Practical rules:
- Reuse computed results: if a function already fetched a snapshot, don’t re-fetch it in telemetry/emit paths—pass or cache the snapshot.
- Constrain discovery: when enumerating remote state, don’t fetch everything by default; limit to the minimal needed refs (e.g., default/upstream branch) or rely on cheaper local refs.
- Guard background side effects: in UI hydration or “tail”/handoff states, ensure suppression/gating prevents extra renders or avoidable network rehydration.
- Reduce IO amplification: replace per-file/per-process git spawning with batched or streaming approaches; batch when you can.
- Prewarm only the correct scope/key: warm the workspace/service you’ll actually use; warming the wrong key wastes startup time.

Example (reuse a single snapshot for both message + telemetry):
```ts
async function fallbackCaptureAndTelemetry() {
  const terminalSnapshot = await getLatestTerminalOutput();
  // emit message based on snapshot
  emitFallbackMessage(terminalSnapshot);
  // reuse the same snapshot-derived info for telemetry
  telemetryService.captureTerminalOutputFailure(terminalSnapshot.timedOut ? 'TIMEOUT' : 'OTHER');
}
```

If you can’t reuse, explicitly justify the extra cost and add a constraint (limit, debounce, early return, or state gate) matching the minimal behavior you need for correctness.