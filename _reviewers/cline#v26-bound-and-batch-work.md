---
title: Bound and Batch Work
description: 'Prefer performance-safe patterns for expensive external work (git/network/terminal
  captures/process management): scope/bound what you fetch, batch operations to reduce
  process spawning, avoid duplicate async capture calls, and clean up resources on
  fallback/early resolve.'
repository: cline/cline#v26
label: Performance Optimization
language: TypeScript
comments_count: 4
repository_stars: 70893
---

Prefer performance-safe patterns for expensive external work (git/network/terminal captures/process management): scope/bound what you fetch, batch operations to reduce process spawning, avoid duplicate async capture calls, and clean up resources on fallback/early resolve.

Use this checklist:
- Limit scope before confirmation: don’t enumerate all remote refs/heads unless required; prefer default/upstream branch refs or local remote-tracking data.
- Batch external operations: replace “N processes per file” patterns with one batched command (e.g., `git cat-file --batch`).
- Reuse expensive results: if one function already captured a snapshot for telemetry/rendering, pass/reuse it instead of calling again.
- Cleanup on early settle: when resolving on timeout/fallback, remove listeners/timers and close/detach inherited stdio so background children can’t keep the host alive or continue writing.

Example (avoid duplicate capture in a fallback path):
```ts
async function fallbackCapture(telemetry: any) {
  // Capture once
  const terminalSnapshot = await getLatestTerminalOutput();

  // Reuse the same snapshot for the user-visible message
  // and for telemetry success/failure decisions.
  const fallbackMessage = terminalSnapshot.message;
  telemetry.captureTerminalOutput(terminalSnapshot.ok ? 'success' : 'failure', terminalSnapshot);

  return fallbackMessage;
}
```

These rules reduce network/process load, clipboard/IO side effects, and “zombie” resource retention, improving latency and stability.