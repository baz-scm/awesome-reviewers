---
title: Minimize External Work
description: Default to doing the smallest possible amount of external work (git/network/process/UI
  side effects), and never repeat expensive operations when you already have the result.
repository: cline/cline#v30
label: Performance Optimization
language: TypeScript
comments_count: 7
repository_stars: 70894
---

Default to doing the smallest possible amount of external work (git/network/process/UI side effects), and never repeat expensive operations when you already have the result.

Apply these rules:
- **Scope heavy discovery**: when listing git/network data, prefer a minimal subset (e.g., default/upstream branch or local remote-tracking refs) instead of “all heads”.
- **Gate remote/background side effects**: avoid opening remote sessions or spawning sandboxes during sidebar hydration or other non-user-driven flows; warm/spawn only for the correct, user-relevant workspace key.
- **Reuse results**: if a function already fetched a snapshot/result, pass it through—don’t fetch again for telemetry/secondary logic.
- **Remove redundancy**: delete repeated checks/computations that already ran in the same request path.
- **Keep bounded/limited IO**: when downloading/parsing large artifacts, stop once limits are exceeded and cancel promptly.

Example (reuse a fetched snapshot instead of calling twice):
```ts
async function fallbackCapture() {
  // Fetch once
  const terminalSnapshot = await getLatestTerminalOutput();

  // Reuse for both emitted message and telemetry
  emitFallbackMessage(terminalSnapshot);
  telemetryService.captureTerminalOutputSuccess(terminalSnapshot);
}
```

Outcome: lower latency, fewer side effects (clipboard/capture/network/Hubs), reduced memory/CPU churn, and more consistent telemetry because all logic derives from the same data.