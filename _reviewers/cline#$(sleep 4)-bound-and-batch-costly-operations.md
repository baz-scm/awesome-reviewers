---
title: Bound and batch costly operations
description: Operations that touch the filesystem, spawn processes, or hit the network
  must scale with the size of the actual work being done, not with the size of the
  whole repository, directory, or dataset — and must never repeat the same expensive
  call when the result can be reused.
repository: cline/cline#$(sleep 4)
label: Performance Optimization
language: TypeScript
comments_count: 7
repository_stars: 70978
---

Operations that touch the filesystem, spawn processes, or hit the network must scale with the size of the actual work being done, not with the size of the whole repository, directory, or dataset — and must never repeat the same expensive call when the result can be reused.

Concretely:
- Prefer diff-based or targeted queries over full scans. For example, computing a checkpoint diff with `git diff --raw` against changed paths scales with the number of changes, whereas a full `git ls-tree -r` walk scales with total repo size; the latter should be avoided when a cheaper, change-scoped alternative exists.
- Batch many small operations into one call instead of spawning a process (or making a network/I/O call) per item. Reading N file blobs via a single `git cat-file --batch` call avoids spawning N processes, which can otherwise flood the host (e.g., thousands of concurrent/zombie processes on repos with many untracked files).
- Never fetch or compute more than needed "just in case." Avoid eagerly fetching full remote history (e.g., all remote heads) before a user has confirmed an action; fetch lazily or only the refs actually required, and skip the fetch entirely when local state already proves what's needed.
- Cache and reuse the result of an expensive call within a single operation instead of invoking it twice. If a helper (e.g., a terminal-output snapshot or clipboard round-trip) already produces the value you need, have it return that value for reuse rather than calling it again for a second purpose, which doubles latency and risks divergent results.
- When an operation can't be made proportional to work size, impose an explicit, documented bound (max file count, max file size, max bytes read) so cost is capped and predictable, and reads are still correct within that cap.
- Prefer pre-warming or caching expensive setup (e.g., sandbox/service startup) behind a single guarded trigger (e.g., "once per workspace") rather than paying the cost repeatedly or on every poll.
- Validate performance claims with realistic measurements (e.g., actual process counts on a large real-world workspace) when unit-level mocking of I/O/process primitives would be impractical or fragile.

Example — batching instead of per-item spawning:
```ts
// Before: one `git show` process per file, run concurrently
const contents = await Promise.all(paths.map((p) => runGit(cwd, ["show", `${ref}:${p}`])));

// After: one process for all files
const pending = execFile("git", ["-C", cwd, "cat-file", "--batch"], { encoding: "buffer" });
pending.child.stdin?.end(oids.join("\n") + "\n");
const { stdout } = await pending; // parse once
```

Apply this standard whenever introducing code that walks a repository/directory tree, spawns subprocesses, fetches remote data, or otherwise performs I/O whose cost could grow unboundedly with the size of the workspace rather than the size of the change being processed.</description>
</invoke>
