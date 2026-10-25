---
title: Avoid redundant expensive work
description: Expensive work (external process spawning, large downloads, clipboard
  round-trips, remote session hydration, heavy git queries) must not be duplicated
  accidentally. Prefer batching/streaming and ensure you fetch/compute once, then
  reuse the result for telemetry, success/failure, and downstream logic. Also ensure
  event listeners and background effects don’t...
repository: CLINE/CLINE
label: Performance Optimization
language: TypeScript
comments_count: 6
repository_stars: 70837
---

Expensive work (external process spawning, large downloads, clipboard round-trips, remote session hydration, heavy git queries) must not be duplicated accidentally. Prefer batching/streaming and ensure you fetch/compute once, then reuse the result for telemetry, success/failure, and downstream logic. Also ensure event listeners and background effects don’t multiply the number of executions.

Apply this as a checklist:
- **Fetch/compute once:** Don’t call the same expensive “get latest output”/“read results” function twice in the same code path; reuse the snapshot.
- **Batch or stream for many items:** For N files/blobs, avoid N git processes; use `git cat-file --batch` or equivalent.
- **Short-circuit with limits:** Enforce max sizes and stop reading once exceeded (don’t fully buffer an unbounded response).
- **Prevent multiplicative effects:** Register listeners once; ensure retries don’t stack listeners. Avoid background hydration that opens network connections.

Example (reuse snapshot instead of double capture):
```ts
async function fallbackAndTelemetry() {
  const snapshot = await returnCurrentTerminalContents(); // single clipboard capture
  telemetryService.captureTerminalOutputFailure(/*reason*/, snapshot);
}
```

Example (batch git blob reads):
```ts
async function readBlobsBatch(cwd: string, oids: Iterable<string>) {
  const unique = [...new Set(oids)];
  if (!unique.length) return new Map();
  const { stdout } = await execFile('git', ['-C', cwd, 'cat-file', '--batch'], {
    windowsHide: true,
    encoding: 'buffer',
    maxBuffer: Number.POSITIVE_INFINITY,
  });
  // parse once, then populate map
}
```