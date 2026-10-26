---
title: Avoid redundant expensive work
description: For performance-critical paths, ensure you (1) don’t broaden work scope
  until it’s actually needed, and (2) don’t repeat costly I/O/captures or derived
  computations.
repository: cline/cline#v2
label: Performance Optimization
language: TypeScript
comments_count: 5
repository_stars: 70861
---

For performance-critical paths, ensure you (1) don’t broaden work scope until it’s actually needed, and (2) don’t repeat costly I/O/captures or derived computations.

Practical rules:
- **Deduplicate costly calls**: if a function already fetches a snapshot, reuse it for telemetry/UI rather than calling the fetch again.
- **Limit expensive queries**: when listing remote refs/commit SHAs, fetch only what you truly need (e.g., upstream/default branch) or use local tracking refs; avoid “fan-out” before user confirmation.
- **Remove redundant prechecks**: if checks already ran in a previous loop, don’t repeat them.
- **Gate side effects on partial state**: when streams emit partial updates, explicitly gate effect/visibility logic to prevent avoidable insertions/removals.

Example (dedupe telemetry capture):
```ts
// Bad: second snapshot capture causes duplicated clipboard/IO side-effects
telemetryService.captureTerminalOutputFailure(
  TerminalOutputFailureReason.TIMEOUT,
);
await returnCurrentTerminalContents();

// Better: capture once, reuse for both fallback message and telemetry
const terminalSnapshot = await getLatestTerminalOutput();
await returnCurrentTerminalContentsFromSnapshot(terminalSnapshot);
telemetryService.captureTerminalOutputFailure(
  TerminalOutputFailureReason.TIMEOUT,
  terminalSnapshot.success,
);
```

Apply this by scanning PRs for repeated `await` of the same expensive operation, broad remote/network calls executed before confirmation, and duplicate loops/effects that can be gated or removed.