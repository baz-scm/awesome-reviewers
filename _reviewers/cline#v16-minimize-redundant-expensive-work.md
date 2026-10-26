---
title: Minimize redundant expensive work
description: When adding features, avoid unnecessary expensive computation, network
  calls, enumeration, and duplicate side effects. Prefer (a) reusing already-computed
  results and (b) gating/limiting work to the smallest necessary set.
repository: cline/cline#v16
label: Performance Optimization
language: TypeScript
comments_count: 7
repository_stars: 70882
---

When adding features, avoid unnecessary expensive computation, network calls, enumeration, and duplicate side effects. Prefer (a) reusing already-computed results and (b) gating/limiting work to the smallest necessary set.

Apply these rules:
- Reuse computed snapshots/results across code paths (telemetry, UI rendering, success/failure decisions). Don’t call the same expensive capture/fetch twice.
- Gate heavy work behind the correct conditions (e.g., only enumerate remote heads needed for the current preview; only open remote sessions on explicit user actions; suppress UI loaders when provisioning handoff is in progress).
- Limit enumeration of large state (e.g., remote branches/heads) to a focused subset (upstream/default branch) or local refs instead of “all heads”.
- Ensure performance warm-ups are effective: warm the correct workspace/service key; otherwise you pay cost without benefit.

Example (reuse terminal snapshot once):
```ts
// BEFORE: capture twice
const msg = await buildFallbackMessage();
telemetry.captureTerminalOutputFailure(await getLatestTerminalOutput());

// AFTER: capture once, reuse
const terminalSnapshot = await getLatestTerminalOutput();
const msg = buildFallbackMessageFromSnapshot(terminalSnapshot);
telemetry.captureTerminalOutputFailureFromSnapshot(terminalSnapshot, /*reason*/);
```