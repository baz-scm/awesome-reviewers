---
title: Avoid wasteful work
description: When performance-sensitive code calls external systems (Git, clipboard,
  network, filesystem) or does large enumerations, design to (1) avoid duplicated
  expensive calls, (2) bound the scope of what you enumerate/fetch, and (3) enforce
  strict resource limits with graceful partial results.
repository: cline/cline#v4
label: Performance Optimization
language: TypeScript
comments_count: 4
repository_stars: 70864
---

When performance-sensitive code calls external systems (Git, clipboard, network, filesystem) or does large enumerations, design to (1) avoid duplicated expensive calls, (2) bound the scope of what you enumerate/fetch, and (3) enforce strict resource limits with graceful partial results.

Apply:
- Reuse computed snapshots: if a fallback function already captured terminal output, don’t capture again just for telemetry—pass/reuse the same snapshot.
- Bound Git enumeration: don’t list every remote branch/head when you only need a default/upstream view.
- Batch and limit: replace per-file/per-entry process spawning with batched commands; stream reads and stop once you exceed size/time thresholds.
- Partial success: if output/time/buffer limits are hit, preserve whatever cheap/critical subset you can (e.g., HEAD/branch) instead of failing the whole result.

Example (reuse expensive capture):
```ts
// Bad: captures twice
telemetry.capture(await getLatestTerminalOutput());
const msg = await returnCurrentTerminalContents();

// Good: capture once, reuse snapshot for both telemetry + message
const terminalSnapshot = await getLatestTerminalOutput();
telemetry.captureTerminalOutputFailureAndSuccess(terminalSnapshot);
const msg = formatFallbackMessage(terminalSnapshot);
```