---
title: Batch and cache costly operations
description: 'Design I/O-heavy and subprocess-heavy code paths to scale with the size
  of the actual change or request, not with the total size of the dataset or the number
  of items involved. Concretely:'
repository: cline/cline#"><b>zze3729958
label: Performance Optimization
language: TypeScript
comments_count: 7
repository_stars: 71067
---

Design I/O-heavy and subprocess-heavy code paths to scale with the size of the actual change or request, not with the total size of the dataset or the number of items involved. Concretely:

- Avoid spawning one subprocess (or making one network/filesystem call) per item when a single batched call can do the same work. For example, replace per-file `git show` calls run concurrently with one `git cat-file --batch` call — this turns thousands of concurrent processes into a handful, even if peak memory stays similar.
- Prefer commands/algorithms whose cost is proportional to what changed (e.g. `git diff --raw` over changed paths) rather than ones that walk the entire dataset (e.g. full-tree `git ls-tree -r` of a large repo).
- Don't fetch or read more than is needed to answer the question at hand (e.g. don't fetch every remote branch's history just to check if local commits are already published; limit fetches to the relevant ref when possible).
- Cache and reuse the result of an expensive call instead of invoking it twice. If a helper already fetches/computes a value internally, have it return that value so callers can reuse it instead of re-fetching (as seen with duplicated terminal-snapshot captures and duplicated clipboard round-trips).
- Defer expensive synchronous work (e.g. blocking `execSync` calls) until it's actually required, and cache the result, instead of doing it eagerly at module load or startup.
- When synchronous or unbounded work can't be avoided entirely, make it provably bounded (cap file counts/sizes, cap iteration counts) and document why the bound is acceptable for now.
- Validate performance claims against realistic workloads (e.g. a repo with thousands of untracked files) rather than relying on unit tests that can't easily simulate process/resource behavior; mocking child-process spawning or similar low-level APIs for a count-based assertion is usually not worth the added test complexity — prefer a documented manual/benchmark comparison.

Example of batching instead of per-item spawning:
```ts
// Before: one `git show` per file, run concurrently
await Promise.all(paths.map((p) => runGit(cwd, ["show", `${ref}:${p}`])));

// After: one batched call for all blobs
const pending = execFile("git", ["-C", cwd, "cat-file", "--batch"], {
  maxBuffer: Number.POSITIVE_INFINITY,
  encoding: "buffer",
});
pending.child.stdin?.end(oids.join("\n") + "\n");
const { stdout } = await pending; // parse all blobs from one buffer
```