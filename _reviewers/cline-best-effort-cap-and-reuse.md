---
title: Best-effort cap and reuse
description: When code performs expensive IO (git/network/subprocess/clipboard capture),
  it must (1) avoid redundant work, (2) avoid over-scoped enumeration before it’s
  necessary, and (3) degrade gracefully when caps are hit.
repository: CLINE/cline
label: Performance Optimization
language: TypeScript
comments_count: 4
repository_stars: 70839
---

When code performs expensive IO (git/network/subprocess/clipboard capture), it must (1) avoid redundant work, (2) avoid over-scoped enumeration before it’s necessary, and (3) degrade gracefully when caps are hit.

**Apply this standard**
- **Reuse computed snapshots**: if you already fetched a terminal/git snapshot for behavior, reuse the same value for telemetry/derived checks—don’t call the capture function again.
- **Gate heavy Git/network enumeration**: don’t enumerate full remote state (e.g., every remote head SHA) before user confirmation; prefer default/upstream branches or local refs, or defer/limit until needed.
- **Return partial results under limits**: when subprocess output/time/buffer caps are exceeded, preserve the low-cost parts you already know and return a `{ state: "partial" }` (or equivalent) instead of failing into `{ state: "unavailable" }`.
- **Centralize preflight checks**: avoid reading the same repo twice with different rules in separate layers; move shared logic into one place.

**Example pattern (reuse snapshot once)**
```ts
// BAD: captures twice (expensive clipboard round-trip)
await returnCurrentTerminalContents();
telemetry.captureTerminalOutputFailure(TerminalOutputFailureReason.TIMEOUT);

// GOOD: capture once and reuse
const snapshot = await returnCurrentTerminalContents(); // should return what it fetched
telemetry.captureTerminalOutputFailure(
  snapshot.success
    ? TelemetryReason.SUCCESS
    : TelemetryReason.TIMEOUT,
  snapshot
);
```

**Example pattern (partial under caps)**
```ts
const { stdout, state } = await readGitSnapshotWithCaps(cwd);
if (state === 'partial') {
  emitPartialSnapshot({ /* include HEAD/branch, omit noisy sections */ });
} else {
  emitFullSnapshot(stdout);
}
```