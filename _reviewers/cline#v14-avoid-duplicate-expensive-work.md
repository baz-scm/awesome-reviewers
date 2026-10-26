---
title: Avoid duplicate expensive work
description: When a code path performs an expensive operation (spawning processes,
  remote enumeration/fetch, clipboard capture, streaming waits), ensure it happens
  once per intent and is properly scoped.
repository: cline/cline#v14
label: Performance Optimization
language: TypeScript
comments_count: 5
repository_stars: 70876
---

When a code path performs an expensive operation (spawning processes, remote enumeration/fetch, clipboard capture, streaming waits), ensure it happens once per intent and is properly scoped.

Apply these rules:
1) Reuse computed results/snapshots
- If you already captured terminal output (or any derived snapshot), pass/reuse it for telemetry and downstream logic. Never re-capture just to compute a different boolean.

```ts
// Bad: captures terminal output twice (doubles clipboard round-trips)
const msg = await returnCurrentTerminalContents();
telemetry.captureTerminalOutputFailure();

// Good: capture once, reuse everywhere
const terminalSnapshot = await returnCurrentTerminalContents(); // should internally capture+return snapshot
telemetryService.captureTerminalOutputFailure(
  terminalSnapshot.wasTimeout ? reason : otherReason,
  terminalSnapshot,
);
```

2) Batch or eliminate N+1 process patterns
- Prefer single-process batch operations over per-file `git show` / per-item subprocess loops (e.g., `git cat-file --batch`).

3) Bound “enumerate everything” remote work
- Don’t fetch all branch/head SHAs or download large histories just to list items; limit to a default/upstream target or use lighter local tracking refs.

4) Treat streaming/remote delays as first-class
- Timeouts like “first chunk” must account for models that legitimately think without emitting streamed deltas; gate or lengthen defaults to avoid aborting valid work.

5) Prevent user-driven thrash during long waits
- If locks/waits can be noticeable on slow networks, use a pending UI state and coalesce rapid toggles so repeated user actions don’t create extra work or confusing intermediate states.

This standard reduces CPU/process churn, avoids doubled I/O, minimizes network/history downloads, and prevents user-visible latency/path divergence.