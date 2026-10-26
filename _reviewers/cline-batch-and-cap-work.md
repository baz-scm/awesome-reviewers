---
title: Batch and Cap Work
description: For performance-critical code, avoid unbounded or duplicated expensive
  work. Prefer (1) reuse of already-computed snapshots/results, (2) batching instead
  of per-item subprocess calls, and (3) strict size/time caps with streaming and early
  termination.
repository: Cline/Cline
label: Performance Optimization
language: TypeScript
comments_count: 6
repository_stars: 70840
---

For performance-critical code, avoid unbounded or duplicated expensive work. Prefer (1) reuse of already-computed snapshots/results, (2) batching instead of per-item subprocess calls, and (3) strict size/time caps with streaming and early termination.

Apply:
1) Reuse computed snapshots/results
- If you need a fallback message, telemetry, and success criteria, compute the snapshot once and derive all downstream values from that single result.

2) Batch expensive subprocess operations
- Replace per-file `git show`/similar patterns with batched or bulk operations (e.g., `ls-tree` + `git cat-file --batch`) to avoid spawning a git process per file.

3) Enforce caps with streaming/early stop
- For downloads and large payload reads, stream and stop as soon as you cross a configured limit; do not buffer entire responses when you only need to reject/skip oversized content.

Example (batching + single pass concept):
```ts
async function readBlobsBatch(cwd: string, oids: Iterable<string>): Promise<Map<string, string>> {
  const contents = new Map<string, string>();
  const input = [...new Set(oids)].join("\n");
  if (!input) return contents;

  // One git process for many objects.
  const pending = execFile("git", ["-C", cwd, "cat-file", "--batch"], {
    windowsHide: true,
    maxBuffer: Number.POSITIVE_INFINITY,
    encoding: "buffer",
  });

  pending.child.stdin?.end(`${input}\n`);
  const { stdout } = await pending;
  // Parse stdout into contents (implementation omitted)
  return contents;
}
```

Example (reuse computed snapshot; avoid duplicate capture):
```ts
const snapshot = await getLatestTerminalOutput();
telemetryService.captureTerminalOutputFailure(reason, { snapshot });
await returnCurrentTerminalContentsFromSnapshot(snapshot);
```

Checklist for code review:
- Are any expensive captures/computations called more than once per request?
- Are we spawning subprocesses in a tight loop instead of batching/bulk querying?
- Are we reading unbounded data (no early stop / no size caps)?
- Do we have explicit caps/timeouts and sensible skip behavior for oversized outputs?