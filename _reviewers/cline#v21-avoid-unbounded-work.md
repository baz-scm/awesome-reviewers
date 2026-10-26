---
title: Avoid Unbounded Work
description: When code performs expensive I/O (git, network, terminal/clipboard capture,
  large file listings), ensure it’s (1) scoped to the minimum required, (2) coalesced/batched
  to avoid N-process or N-roundtrips, (3) not duplicated, and (4) capped with graceful
  partial degradation.
repository: cline/cline#v21
label: Performance Optimization
language: TypeScript
comments_count: 5
repository_stars: 70886
---

When code performs expensive I/O (git, network, terminal/clipboard capture, large file listings), ensure it’s (1) scoped to the minimum required, (2) coalesced/batched to avoid N-process or N-roundtrips, (3) not duplicated, and (4) capped with graceful partial degradation.

Practical rules:
- Scope: don’t enumerate “everything” (e.g., all remote heads) unless strictly required—prefer default/upstream branch data or local remote-tracking refs.
- Coalesce/batch: prefer single-process or batched commands (e.g., `git cat-file --batch`) over per-file `git show`/spawning many git processes.
- Reuse results: if you compute a snapshot (terminal output, git status, etc.), reuse it for telemetry/logic—do not re-capture.
- Cap: enforce timeouts/maxBuffer/max bytes. If limits are reached, return a `{ state: "partial" }` result (or equivalent) rather than dropping the whole operation.

Example (reuse expensive capture):
```ts
// Compute once
const terminalSnapshot = await getLatestTerminalOutput();
// Reuse for fallback message + telemetry decision
telemetryService.captureTerminalOutputFailure(
  terminalSnapshot.success ? undefined : TerminalOutputFailureReason.TIMEOUT,
);
await returnCurrentTerminalContentsFromSnapshot(terminalSnapshot);
```