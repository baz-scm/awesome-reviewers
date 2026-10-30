---
title: Eliminate redundant expensive work
description: 'Profile for and eliminate repeated or unbounded expensive operations
  instead of letting them scale linearly with data size, call frequency, or item count.
  Concretely:'
repository: 'cline/cline#

  zzprobe3b82974b: x'
label: Performance Optimization
language: TypeScript
comments_count: 7
repository_stars: 71067
---

Profile for and eliminate repeated or unbounded expensive operations instead of letting them scale linearly with data size, call frequency, or item count. Concretely:

- **Batch external calls instead of spawning per item.** Replace per-file/per-item subprocess or I/O calls with a single batched call (e.g. one `git cat-file --batch` instead of one `git show` per file). A workspace with 3,000 untracked files went from 3,051 concurrent processes to 6 total after batching — verify such fixes against realistic workloads rather than brittle mocks of `child_process`.
- **Reuse already-computed results instead of recomputing them.** If a helper already fetched/produced a value internally, have it return that value for the caller to reuse rather than invoking the same expensive path a second time. For example, a terminal fallback that already captured output via `getLatestTerminalOutput()` should return that snapshot so telemetry doesn't trigger a second full clipboard round-trip:
  ```ts
  // Bad: duplicates the expensive capture
  await returnCurrentTerminalContents()
  const snapshot = await getLatestTerminalOutput() // redundant round-trip

  // Good: capture once, reuse everywhere
  const snapshot = await returnCurrentTerminalContents() // returns what it fetched
  telemetryService.capture(snapshot)
  ```
- **Use skip-ahead/short-circuit logic instead of brute-force iteration** when scanning for a match (e.g. a cron scheduler should jump to the next plausible date instead of checking every minute), especially when the slow path is also on a hot/validation path.
- **Defer expensive synchronous work off the critical startup/event-loop path.** Lazily compute and cache values (e.g. console encoding detection) on first use rather than blocking module load or the main thread.
- **Throttle or coalesce high-frequency, non-critical triggers** that drive expensive work (e.g. rebuilding a summary object), while ensuring the latest/durable event is still flushed so no information is lost.

When optimizing, measure the real bottleneck (process counts, call counts, wall-clock time on representative inputs) rather than micro-benchmarking in isolation, and bound work (e.g. size caps before reading blobs) where unbounded growth is possible.