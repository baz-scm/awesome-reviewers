---
title: Scope and dedupe expensive operations
description: 'Design expensive operations (filesystem walks, git/process spawns, network
  fetches, clipboard round-trips) to scale with the amount of work actually needed,
  not with the size of the whole repository, directory tree, or remote. Prefer diff-based
  or targeted queries over full scans: e.g. use `git diff --raw` against changed paths
  instead of `git ls-tree -r`...'
repository: cline/cline#中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中
label: Performance Optimization
language: TypeScript
comments_count: 6
repository_stars: 70986
---

Design expensive operations (filesystem walks, git/process spawns, network fetches, clipboard round-trips) to scale with the amount of work actually needed, not with the size of the whole repository, directory tree, or remote. Prefer diff-based or targeted queries over full scans: e.g. use `git diff --raw` against changed paths instead of `git ls-tree -r` over the entire tree, and avoid fetching every remote head just to check if history is already published when a narrower check (comparing against the known upstream ref) would suffice.

Never duplicate a costly call when the result can be captured once and reused. If a helper (like `returnCurrentTerminalContents()`) already fetches a snapshot internally, have it return that snapshot instead of making the caller re-fetch it, and derive every downstream value (telemetry, success flags) from the single captured result:

```ts
// Bad: fetches the terminal snapshot twice
await returnCurrentTerminalContents() // fetches + emits internally
const snapshot = await getLatestTerminalOutput() // fetches again

// Good: fetch once, reuse everywhere
const snapshot = await returnCurrentTerminalContents() // now returns what it fetched
telemetryService.captureResult(snapshot)
```

Similarly, avoid redoing work that was already done and cached (e.g. don't re-truncate/re-serialize large tool results on every request once they've been saved at tool completion), and make sure any process that spawns subprocesses or writes temp/cache files has a disposal or bounding strategy so usage doesn't grow unbounded (stale directories, zombie processes, runaway concurrent spawns).

When a change targets a hot path, validate the improvement with a realistic benchmark against representative data (e.g., a repo with thousands of files/branches) rather than relying on intuition alone, and document the before/after cost (process counts, fetch sizes, latency) in the PR so reviewers can confirm the fix actually bounds the cost.