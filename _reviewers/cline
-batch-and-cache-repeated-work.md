---
title: Batch and cache repeated work
description: 'When an operation runs once per item, per request, or per turn, check
  whether the per-call cost can be amortized instead of repeated: spawning a subprocess
  for every file, re-fetching data that was already fetched moments ago, or rewriting
  the same data on every subsequent request all scale badly and add avoidable latency.'
repository: 'cline/cline

  '
label: Performance Optimization
language: TypeScript
comments_count: 5
repository_stars: 70942
---

When an operation runs once per item, per request, or per turn, check whether the per-call cost can be amortized instead of repeated: spawning a subprocess for every file, re-fetching data that was already fetched moments ago, or rewriting the same data on every subsequent request all scale badly and add avoidable latency.

Concrete patterns to apply:
- Batch subprocess calls instead of forking one per item. Replace a loop of `git show <ref>:<path>` per file with a single `git cat-file --batch` call fed all the OIDs at once, so process-spawn overhead doesn't scale with the number of files.
- Don't fetch the same snapshot twice. If a fallback helper already captures and returns a value internally (e.g. `getLatestTerminalOutput()` inside `returnCurrentTerminalContents()`), have it return that value and reuse it for logging/telemetry rather than issuing the same expensive round-trip (clipboard selection + copy + read) a second time.
- Do expensive side effects (writing large payloads to disk, truncating/annotating oversized results) once at creation time, and persist the result, rather than redoing the work on every subsequent read, resume, or request.
- When synchronous or unbounded work is unavoidable (e.g. reading repo convention files), cap it with explicit size/count limits and cache results keyed by something cheap to check (like file mtime) so repeat calls are near-free.

Example of batching instead of per-item subprocess calls:
```ts
// Before: one git process per file
for (const path of changedPaths) {
  contents.set(path, await runGit(cwd, ["show", `${ref}:${path}`]));
}

// After: one batched process for all files
const input = [...oids].join("\n");
const { stdout } = await execFile("git", ["-C", cwd, "cat-file", "--batch"], { input });
```

Before merging, ask whether a loop or fallback path triggers an expensive operation more times than necessary, and consolidate it into a single batched or cached call.