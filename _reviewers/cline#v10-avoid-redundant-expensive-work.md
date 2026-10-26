---
title: Avoid redundant expensive work
description: Before adding new functionality, ensure you’re not repeating costly external
  work (process spawning, network/git reads, clipboard/terminal captures) or doing
  it too early.
repository: cline/cline#v10
label: Performance Optimization
language: TypeScript
comments_count: 6
repository_stars: 70869
---

Before adding new functionality, ensure you’re not repeating costly external work (process spawning, network/git reads, clipboard/terminal captures) or doing it too early.

Apply these rules:
- **Reuse computed results**: if a function already fetches data (e.g., terminal snapshot), use that same value for telemetry/UI instead of fetching again.
- **Batch external calls**: replace “one git process per file” patterns with “one git process for many items” (`ls-tree` + `cat-file --batch`, etc.).
- **Scope/limit pre-approval operations**: don’t enumerate large remote sets until the user confirms; prefer default/upstream branch targets or local refs.
- **Gate expensive UI/state transitions**: when partial/provisioning handoffs occur, ensure loader visibility conditions are correctly suppressed to avoid churn.
- **Centralize repo checks**: avoid reading the same repo twice in different layers with conflicting rules; move checks into the shared preflight layer.

Example (reuse snapshot for telemetry):
```ts
async function captureWithTelemetry(telemetry: any) {
  const terminalSnapshot = await getLatestTerminalOutput(); // fetch once
  if (!terminalSnapshot.trim()) {
    telemetry.captureTerminalOutputFailure('TIMEOUT');
    await returnFromSnapshot(terminalSnapshot);
  }
}
```

Net effect: fewer spawned processes, fewer network/git operations, fewer redundant state updates, and lower latency—without sacrificing correctness.