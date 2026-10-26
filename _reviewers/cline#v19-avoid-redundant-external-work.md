---
title: Avoid redundant external work
description: When code needs an expensive external operation (Git commands, terminal/clipboard
  capture, network calls, large file reads), ensure you do not repeat it and that
  you only fetch/process what you truly need.
repository: cline/cline#v19
label: Performance Optimization
language: TypeScript
comments_count: 4
repository_stars: 70885
---

When code needs an expensive external operation (Git commands, terminal/clipboard capture, network calls, large file reads), ensure you do not repeat it and that you only fetch/process what you truly need.

Practical rules:
- **Reuse results**: If you already computed a snapshot/output for the main logic, reuse it for telemetry, UI messages, and success/failure decisions—don’t call the capture/API again.
- **Scope queries**: Don’t pre-fetch broad/unbounded data (e.g., “all remote heads”) before the user confirms or before you know it’s needed. Prefer default/upstream branches or local refs.
- **Batch and bound**: Replace per-item external calls with batch/one-process approaches (and enforce size caps) to avoid process thrash and excessive memory/CPU.
- **Remove redundant checks**: If earlier loops already verified preconditions, avoid re-running the same checks elsewhere.

Example pattern (reuse a single capture for both fallback and telemetry):
```ts
const snapshot = await returnCurrentTerminalContents(); // should return the already-fetched snapshot
telemetryService.captureTerminalOutputFailure(
  /* reason */ snapshot.timedOut ? 'TIMEOUT' : 'OTHER',
  /* reuse */ snapshot
);
```

If you can’t reuse today, restructure the function so the expensive call happens once and its output is passed to all downstream uses.