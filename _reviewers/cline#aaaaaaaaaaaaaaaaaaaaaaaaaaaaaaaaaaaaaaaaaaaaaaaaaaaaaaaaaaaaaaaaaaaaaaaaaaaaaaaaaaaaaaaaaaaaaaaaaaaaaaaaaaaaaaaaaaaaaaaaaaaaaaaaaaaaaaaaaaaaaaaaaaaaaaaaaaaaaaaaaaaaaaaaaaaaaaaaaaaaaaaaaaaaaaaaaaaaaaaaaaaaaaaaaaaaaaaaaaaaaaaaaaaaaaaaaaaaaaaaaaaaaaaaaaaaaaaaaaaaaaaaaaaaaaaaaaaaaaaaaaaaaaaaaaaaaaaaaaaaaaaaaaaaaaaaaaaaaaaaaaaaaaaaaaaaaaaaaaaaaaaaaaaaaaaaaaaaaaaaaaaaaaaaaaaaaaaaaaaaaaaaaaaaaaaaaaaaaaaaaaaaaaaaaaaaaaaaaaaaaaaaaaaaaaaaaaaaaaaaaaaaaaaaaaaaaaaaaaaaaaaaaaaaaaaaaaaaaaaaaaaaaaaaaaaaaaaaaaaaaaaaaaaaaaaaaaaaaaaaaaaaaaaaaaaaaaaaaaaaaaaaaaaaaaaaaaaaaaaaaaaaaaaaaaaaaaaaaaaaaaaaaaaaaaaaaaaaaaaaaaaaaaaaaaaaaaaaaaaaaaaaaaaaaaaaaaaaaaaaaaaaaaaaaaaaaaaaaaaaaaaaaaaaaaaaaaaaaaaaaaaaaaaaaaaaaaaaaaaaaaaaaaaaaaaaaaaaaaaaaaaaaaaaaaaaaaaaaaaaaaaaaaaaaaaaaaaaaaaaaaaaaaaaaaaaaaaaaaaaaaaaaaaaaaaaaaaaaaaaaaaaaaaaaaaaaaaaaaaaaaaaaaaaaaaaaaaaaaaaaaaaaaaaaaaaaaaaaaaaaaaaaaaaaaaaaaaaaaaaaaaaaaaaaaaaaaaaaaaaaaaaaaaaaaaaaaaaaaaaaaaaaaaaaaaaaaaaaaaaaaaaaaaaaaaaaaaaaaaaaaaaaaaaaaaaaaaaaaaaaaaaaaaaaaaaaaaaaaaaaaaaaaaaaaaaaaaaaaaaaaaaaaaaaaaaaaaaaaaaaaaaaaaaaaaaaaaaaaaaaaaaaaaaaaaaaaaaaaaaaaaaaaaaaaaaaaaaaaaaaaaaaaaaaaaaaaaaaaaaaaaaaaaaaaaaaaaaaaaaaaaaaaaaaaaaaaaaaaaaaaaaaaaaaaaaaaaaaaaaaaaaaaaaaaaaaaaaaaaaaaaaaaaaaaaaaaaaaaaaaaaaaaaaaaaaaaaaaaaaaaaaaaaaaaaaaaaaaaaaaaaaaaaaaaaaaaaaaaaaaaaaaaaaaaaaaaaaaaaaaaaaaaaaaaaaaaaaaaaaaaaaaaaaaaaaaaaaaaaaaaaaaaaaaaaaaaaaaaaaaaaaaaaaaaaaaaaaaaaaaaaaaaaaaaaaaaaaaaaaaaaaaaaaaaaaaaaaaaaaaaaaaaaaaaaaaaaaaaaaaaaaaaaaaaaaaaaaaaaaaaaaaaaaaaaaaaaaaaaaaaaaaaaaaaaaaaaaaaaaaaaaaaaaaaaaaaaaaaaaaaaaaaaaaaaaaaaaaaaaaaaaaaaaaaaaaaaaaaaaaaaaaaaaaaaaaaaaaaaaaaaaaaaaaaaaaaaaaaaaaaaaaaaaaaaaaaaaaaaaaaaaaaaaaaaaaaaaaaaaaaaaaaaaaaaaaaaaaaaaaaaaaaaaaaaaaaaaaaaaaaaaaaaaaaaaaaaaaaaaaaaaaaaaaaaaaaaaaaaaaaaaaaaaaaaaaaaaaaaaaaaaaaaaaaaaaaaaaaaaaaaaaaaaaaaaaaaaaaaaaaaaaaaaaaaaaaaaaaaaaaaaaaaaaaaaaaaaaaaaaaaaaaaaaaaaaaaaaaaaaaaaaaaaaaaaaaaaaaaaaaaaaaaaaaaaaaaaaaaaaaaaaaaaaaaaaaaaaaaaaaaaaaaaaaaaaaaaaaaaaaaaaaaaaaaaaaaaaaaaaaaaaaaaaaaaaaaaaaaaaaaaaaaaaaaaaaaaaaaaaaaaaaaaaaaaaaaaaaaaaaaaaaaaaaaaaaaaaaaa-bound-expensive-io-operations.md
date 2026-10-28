---
title: Bound expensive I/O operations
description: When an operation can scale with input size (number of files, branches,
  remote heads, tool results), make the cost explicit and bounded rather than letting
  it grow unchecked, and avoid repeating expensive work that has already been done.
repository: cline/cline#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
label: Performance Optimization
language: TypeScript
comments_count: 8
repository_stars: 70968
---

When an operation can scale with input size (number of files, branches, remote heads, tool results), make the cost explicit and bounded rather than letting it grow unchecked, and avoid repeating expensive work that has already been done.

- Batch instead of spawning one process/request per item. Spawning a subprocess per file (e.g. `git show` per untracked file) can flood the host with hundreds or thousands of concurrent processes; route them through one batched call instead:
  ```ts
  // Bad: one process per file
  await Promise.all(files.map(f => runGit(cwd, ["show", `${ref}:${f}`])))

  // Good: one batched process for all files
  const pending = execFile("git", ["-C", cwd, "cat-file", "--batch"], { ... })
  pending.child.stdin?.end(oids.join("\n"))
  ```
  Validate the improvement with realistic numbers (e.g. "3,051 concurrent processes reduced to 6") rather than assuming it is better.

- Cap unbounded network/filesystem work explicitly, and document the cap. Prefer fetching only what's needed (the upstream/default branch or local remote-tracking refs) instead of every remote head; cap file counts/sizes read synchronously (e.g. "16 files, 256KB each") so a single call stays small and interruptible-enough for an MVP; cap per-item result sizes but also account for the aggregate when an API can return N items (N × per-item cap can blow past an overall budget — make sure a total-result cap or compaction step still applies).

- Never issue the same expensive call twice when one result can be reused. If a helper already fetches a snapshot/result internally, have it return that value so callers reuse it instead of re-fetching (duplicate clipboard round-trips, duplicate session reads, etc. double latency and can produce inconsistent results between the two calls).

- Guard expensive initialization (warm-up, sandbox start, session host creation) so it runs once per resource/workspace rather than on every poll or every call site, and trigger it from the single chokepoint that sees all code paths (e.g. the shared workspace-adoption hook) instead of duplicating the trigger in every entry point.

- When you intentionally accept a bound instead of fully eliminating a cost (e.g. synchronous reads, a fetch fallback that still touches the network), state the bound and the condition under which it would need revisiting, so the tradeoff is reviewable later.</description>
</invoke>
