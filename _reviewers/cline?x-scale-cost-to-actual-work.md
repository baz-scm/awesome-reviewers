---
title: Scale cost to actual work
description: Avoid operations whose cost scales with the size of the whole dataset
  or repository when only a small subset is actually needed, and never spawn one subprocess/IO
  call per item when a single batched call will do. Before adding a loop that shells
  out, fetches, or reads per file/branch/item, ask whether the operation can be bounded
  to the relevant subset...
repository: cline/cline?x
label: Performance Optimization
language: TypeScript
comments_count: 5
repository_stars: 70983
---

Avoid operations whose cost scales with the size of the whole dataset or repository when only a small subset is actually needed, and never spawn one subprocess/IO call per item when a single batched call will do. Before adding a loop that shells out, fetches, or reads per file/branch/item, ask whether the operation can be bounded to the relevant subset (e.g., diff against a ref instead of listing the entire tree, fetch only the branches actually needed instead of every remote head) or combined into one call (e.g., `git cat-file --batch` instead of one `git show` per file). Concurrent per-item subprocess spawning can silently explode resource usage under real workloads (one review found 3,051 concurrent git processes and 3,046 zombies for a single comparison on a repo with 3,000 untracked files, versus 6 total processes after batching) and should be caught before merging, not after a user reports stalls.

Also avoid redundant duplicate work: if a result (e.g., a terminal snapshot, fetched data, or computed value) is already available from a prior call in the same code path, reuse it instead of recomputing/refetching it. Duplicating an expensive round-trip (such as a clipboard capture or network fetch) not only doubles latency but risks the two results diverging, which can introduce subtle correctness bugs on top of the performance cost.

Example of the pattern to apply:
```ts
// Bad: one subprocess per file, and relisting the whole tree
for (const path of changedPaths) {
  await execFile("git", ["show", `${ref}:${path}`]);
}

// Good: single batched call scaled to the actual diff
const { stdout } = await execFile("git", ["diff", "--raw", "--no-abbrev", ref]);
// then one `git cat-file --batch` call to read all needed blobs
```

When reviewing or writing performance-sensitive code (subprocess orchestration, network fetches, file/tree traversal), verify: (1) the operation's cost is bounded by the amount of actual work/change, not the total repository or dataset size, (2) per-item work is batched into as few calls/processes as practical, and (3) no already-fetched value is being redundantly recomputed elsewhere in the same flow. If a deeper fix (e.g., streaming parsers, shared long-lived connections) adds significant complexity for only a constant-factor gain, it's reasonable to defer it, but the decision and rationale should be documented.</description>
</invoke>
