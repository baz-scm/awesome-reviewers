---
title: Avoid costly redundant work
description: In performance-sensitive code paths, ensure you (1) don’t duplicate expensive
  async computations, (2) don’t do high-fanout git/network work before it’s necessary,
  and (3) when you must cap time/buffer/size, return partial results instead of failing
  or dropping all work.
repository: cline/CLINE
label: Performance Optimization
language: TypeScript
comments_count: 4
repository_stars: 70839
---

In performance-sensitive code paths, ensure you (1) don’t duplicate expensive async computations, (2) don’t do high-fanout git/network work before it’s necessary, and (3) when you must cap time/buffer/size, return partial results instead of failing or dropping all work.

How to apply
- Reuse already-fetched results: if you computed a snapshot/output for control flow, don’t recompute it for telemetry/emission.
- Reduce fan-out: replace per-file/per-branch/per-entry git calls with batched or targeted commands, and prefer “latest/default/upstream only” over enumerating everything.
- Gate heavy work: don’t fetch large/whole-repo metadata until the user confirms the action (or you truly need it).
- Graceful degradation: when timeouts/buffers are hit, preserve whatever you already captured and mark the result as partial rather than discarding everything.

Example patterns
1) Reuse a single terminal snapshot for fallback + telemetry:
```ts
const terminalSnapshot = await returnCurrentTerminalContents(); // change this to return snapshot
telemetryService.captureTerminalOutputFailure(
  terminalSnapshot.isTimeout ? terminalSnapshot.reason : terminalSnapshot.successReason
);
```
If changing the signature isn’t feasible, capture `terminalSnapshot` once at the call site and reuse it for both the emitted message and telemetry.

2) Batch git reads instead of spawning per file:
```ts
const input = [...new Set(oids)].join("\n");
if (!input) return new Map();
const { stdout } = await execFile("git", ["-C", cwd, "cat-file", "--batch"], {
  windowsHide: true,
  maxBuffer: Number.POSITIVE_INFINITY,
  encoding: "buffer",
});
// parse stdout once
```

3) If caps are hit, emit partial telemetry/state rather than `{ state: "unavailable" }`:
```ts
try {
  // expensive read with strict limits
} catch (e) {
  return { state: "partial", headInfo, dirtyFlags: undefined };
}
```

Team standard
- Any new code that runs git/network/clipboard/large parsing in loops must justify the approach (batching/targeting/gating) and explicitly define what happens when caps are reached (partial vs fail).