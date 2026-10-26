---
title: Avoid redundant expensive work
description: Prefer reusing already-computed results and minimizing high-fan-out/high-latency
  external work (process spawns, Git/network calls, clipboard/IO captures). This reduces
  latency, host load, and side effects.
repository: cline/cline#v8
label: Performance Optimization
language: TypeScript
comments_count: 4
repository_stars: 70867
---

Prefer reusing already-computed results and minimizing high-fan-out/high-latency external work (process spawns, Git/network calls, clipboard/IO captures). This reduces latency, host load, and side effects.

Guidelines:
- Reuse captured/derived data: if you already fetched a snapshot, don’t call the same capture again just for telemetry/logic—derive everything from the single result.
- Batch external calls: replace “spawn git per file” patterns with batch/aggregate commands (e.g., `git cat-file --batch`) or equivalent APIs.
- Bound preflight scope: don’t “list everything” from remote (e.g., all remote heads/history) unless required; restrict to default/upstream refs or use cheaper/local tracking refs, and defer costly work until after user confirmation.
- Cap resource usage and cancel early: enforce byte/time limits and stop reading once limits are exceeded.

Example (dedupe expensive capture):
```ts
// BAD: captures twice (two clipboard/IO round-trips)
await returnCurrentTerminalContents();
telemetryService.captureTerminalOutputFailure(reason); // calls getLatestTerminalOutput() again

// GOOD: capture once and reuse
const terminalSnapshot = await getLatestTerminalOutput();
await returnCurrentTerminalContentsFromSnapshot(terminalSnapshot);
telemetryService.captureTerminalOutputFailure(reason, terminalSnapshot);
```

Example (batch Git objects):
- Prefer one `git cat-file --batch` over `Promise.all(files.map(f => git show ref:f)))`, which spawns many git processes and increases host pressure.