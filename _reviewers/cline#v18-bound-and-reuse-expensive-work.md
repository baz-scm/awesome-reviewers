---
title: Bound and Reuse Expensive Work
description: 'When code performs expensive I/O (subprocesses, git/network calls, terminal/workbench
  captures), avoid redundant work and prevent unbounded fan-out.


  Standard:'
repository: cline/cline#v18
label: Performance Optimization
language: TypeScript
comments_count: 3
repository_stars: 70884
---

When code performs expensive I/O (subprocesses, git/network calls, terminal/workbench captures), avoid redundant work and prevent unbounded fan-out.

Standard:
- Reuse outputs you already fetched: if a function/call site already computed a snapshot/string/buffer, pass it through—don’t capture again for telemetry or branching.
- Replace per-item subprocess fan-out with batching: prefer “one git process per operation” (e.g., `cat-file --batch`) over spawning one process per file.
- Scope/limit remote exploration before user confirmation: don’t fetch all remote refs/heads or large histories when you only need a small subset.
- Add hard limits early (timeouts, byte caps, concurrency limits) to prevent runaway memory/network usage.

Example (reuse a captured snapshot instead of re-capturing):
```ts
// Bad: duplicates terminal capture work
// telemetryService.captureTerminalOutputFailure(); -> getLatestTerminalOutput() runs again

// Good: capture once, then derive both telemetry and user-visible fallback
const terminalSnapshot = await getLatestTerminalOutput();
await returnCurrentTerminalContents(terminalSnapshot);
telementryService.captureTerminalOutputFailure(
  TerminalOutputFailureReason.TIMEOUT,
  terminalSnapshot,
);
```

Example (batch git blob reads rather than per-file `git show`):
```ts
// Prefer: ls-tree to collect oids, then one cat-file --batch to read many blobs
const blobs = await listTreeBlobs(cwd, treeish);
const contents = await readBlobs(cwd, blobs.values().map(b => b.oid));
```

Apply this during review by asking: “Is this doing the same expensive capture twice?” and “Is there any unbounded fan-out (per-file/per-ref/per-branch) or remote fetch that could be scoped/limited?”