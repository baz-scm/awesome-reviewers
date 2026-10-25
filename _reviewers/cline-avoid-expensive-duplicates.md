---
title: Avoid Expensive Duplicates
description: When adding telemetry, previews, or fallback paths, ensure you don’t
  (a) repeat expensive work, (b) fetch/scan unbounded amounts of data, or (c) hard-fail
  when size/time limits are exceeded.
repository: ClInE/cLiNe
label: Performance Optimization
language: TypeScript
comments_count: 4
repository_stars: 70838
---

When adding telemetry, previews, or fallback paths, ensure you don’t (a) repeat expensive work, (b) fetch/scan unbounded amounts of data, or (c) hard-fail when size/time limits are exceeded.

Apply these rules:
1) Reuse captured results
- If you already called a function that performs a costly capture/subprocess/clipboard round-trip, reuse its output for both the user-facing emission and any “success/failure” telemetry.

Example pattern (fetch once, reuse):
```ts
// Fetch once
const terminalSnapshot = await getLatestTerminalOutput();

// Emit based on the single snapshot
await returnCurrentTerminalContentsFromSnapshot(terminalSnapshot);

// Telemetry based on the same snapshot
telemetryService.captureTerminalOutputFailure(
  terminalSnapshot.state === "ok" ? /*...*/ : /*...*/,
);
```
(If the existing API can’t take a snapshot, refactor so the snapshot is computed once and shared.)

2) Bound “wide” Git/remote operations
- Avoid listing *all* remote heads or downloading large histories when you only need one branch or a small subset.
- Prefer upstream/default branch targets or local remote-tracking refs over enumerating every head.

3) Degrade gracefully under limits
- If subprocess output could exceed buffer/timeout (e.g., large repo status), don’t drop everything.
- Return `{ state: "partial" }` (preserving critical fields like HEAD/branch) when limits are hit, so downstream can still function.

4) Gate unnecessary work during transitional UI states
- During handoffs/optimistic transitions, ensure your combined “should render loader” condition correctly suppresses avoidable loader insertion/removal.

These practices reduce latency, avoid side-effect duplication, and prevent expensive tasks from causing `{ state: "unavailable" }` or UI churn.