---
title: Avoid redundant expensive work
description: When code triggers expensive operations (spawning external processes,
  fetching large git metadata, network/Hub rehydration, clipboard round-trips, or
  background connections), ensure you (1) batch/limit work, (2) don’t duplicate the
  same expensive call in multiple places (especially for telemetry/secondary consumers),
  and (3) gate side effects so they only...
repository: cline/cline#v1
label: Performance Optimization
language: TypeScript
comments_count: 7
repository_stars: 70862
---

When code triggers expensive operations (spawning external processes, fetching large git metadata, network/Hub rehydration, clipboard round-trips, or background connections), ensure you (1) batch/limit work, (2) don’t duplicate the same expensive call in multiple places (especially for telemetry/secondary consumers), and (3) gate side effects so they only run when truly needed.

Guidelines
- Batch and reduce process calls: prefer a single “bulk” command over per-item calls (e.g., `git cat-file --batch` instead of one `git show` per file).
- Limit scope of discovery: avoid fetching/iterating over unbounded remote data when only a subset is needed (e.g., restrict remote heads to upstream/default or local refs).
- Reuse fetched results: if you already captured data (stdout/snapshots), pass it to telemetry/UI logic instead of capturing again.
- Centralize preflight to prevent repeated repository reads across layers.
- Gate side effects: suppress UI/network effects during known transient states (handoffs, provisioning tails) rather than “letting optimistic/partial state” cause extra work.

Example (reuse a captured snapshot instead of recapturing)
```ts
async function fallbackWithTelemetry() {
  // Single expensive capture
  const terminalSnapshot = await getLatestTerminalOutput();

  // Use the same snapshot for both the model message and telemetry
  telemetryService.captureTerminalOutputFailure(TerminalOutputFailureReason.TIMEOUT, {
    snapshot: terminalSnapshot,
  });

  await returnCurrentTerminalContentsFromSnapshot(terminalSnapshot);
}

async function returnCurrentTerminalContentsFromSnapshot(snapshot: string) {
  // build the fallback message from the already-fetched snapshot
  // ...
}
```

Apply this standard by default during code reviews: ask “Is this expensive operation run more times than necessary?”, “Can it be batched/limited?”, and “Are there conditions where this side effect should be suppressed?”