---
title: Limit and reuse expensive calls
description: When code performs expensive work (external processes like Git, network/ref
  discovery, clipboard/terminal capture, large filesystem scans, repeated validation
  loops), ensure it is (1) batched or aggregated to avoid per-item spawning, (2) limited
  to the minimum required scope, and (3) reused across telemetry/UI/logging paths
  instead of recomputed.
repository: cline/cline#v5
label: Performance Optimization
language: TypeScript
comments_count: 4
repository_stars: 70864
---

When code performs expensive work (external processes like Git, network/ref discovery, clipboard/terminal capture, large filesystem scans, repeated validation loops), ensure it is (1) batched or aggregated to avoid per-item spawning, (2) limited to the minimum required scope, and (3) reused across telemetry/UI/logging paths instead of recomputed.

Practical checks to apply in code review:
- **No duplicate captures/fetches**: If a function already computed a snapshot/result for the main path, telemetry should reuse it rather than calling the capture/fetch again.
- **Avoid eager “enumerate everything” ref discovery**: Don’t fetch all remote heads/SHAs if only the default/upstream branch (or a capped set) is needed.
- **Prefer one aggregated process** over many per-file/per-entry commands (e.g., Git batch mode instead of `Promise.all` of `git show`).
- **Remove redundant work**: If disconnect/pending checks already ran while building a list/set, don’t rerun the same checks in a second loop.

Example pattern (reuse computed snapshot):
```ts
// Compute once
const terminalSnapshot = await getLatestTerminalOutput();
// Use for both emitted message and telemetry
telemetryService.captureTerminalOutputFailure(
  TerminalOutputFailureReason.TIMEOUT,
  terminalSnapshot,
);
await emitFallbackMessageFromSnapshot(terminalSnapshot);
```

Example pattern (batch/aggregate external calls):
```ts
// Instead of spawning `git show ref:path` per file,
// build a set of oids and fetch all contents in one batch call.
const oids = [...new Set(mapOfOids.keys())];
const { stdout } = await execFile("git", ["-C", cwd, "cat-file", "--batch"], { encoding: "buffer" });
// parse stdout once; skip/limit oversized blobs before storing.
```

This guideline directly targets performance bottlenecks by preventing unnecessary scaling with repo size and avoiding repeated costly side effects.