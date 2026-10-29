---
title: Avoid redundant expensive work
description: 'Before adding code that touches disk, spawns a subprocess, or makes
  a network/git call, check whether the result is already available or could be reused,
  and scope the work to only what''s needed:'
repository: cline/cline#1
label: Performance Optimization
language: TypeScript
comments_count: 6
repository_stars: 71024
---

Before adding code that touches disk, spawns a subprocess, or makes a network/git call, check whether the result is already available or could be reused, and scope the work to only what's needed:

- **Don't repeat an expensive call when the result already exists.** If a helper already computed or fetched a value, have it return that value instead of recomputing it. For example, if `returnCurrentTerminalContents()` already calls `getLatestTerminalOutput()` internally, don't call `getLatestTerminalOutput()` again at the call site for telemetry — reuse the same snapshot so the cost (and any side effects like clipboard round-trips) isn't paid twice and the two readings can't diverge.
- **Batch instead of looping subprocess/network calls per item.** Spawning one `git show` or one API call per file/branch floods the host and scales linearly with repo/workspace size. Prefer a single batched call (e.g. `git cat-file --batch`) over many individual spawns.
- **Scope fetches/queries to what's actually required**, not everything available. Fetching every remote branch's history just to check if one commit is published, for instance, downloads far more than needed on large repos — prefer checking local/remote-tracking refs or the specific branch in question first, and only fall back to a wider fetch when necessary.
- **Don't rewrite or recompute data that doesn't change.** Persist expensive results once (e.g. truncated/large tool output) and reference them afterward instead of regenerating or rewriting them on every subsequent request.
- **Decouple expensive or blocking work from hot/critical paths.** Prewarming, encoding detection, or other setup work should be triggered by its own dedicated event/entry point rather than piggybacking on an unrelated handler, and should be deferred (lazy-initialized) until actually needed rather than run eagerly at startup or module load.
- **Watch for algorithmic shortcuts being applied inconsistently.** If an optimization (e.g. skipping ahead instead of scanning minute-by-minute) is applied for one code path but not another that hits the same bottleneck (e.g. the timezone-aware branch), extend it so all paths get the same complexity improvement.

When reviewing performance-sensitive code, trace each expensive operation back to confirm it runs exactly once per logical need, is appropriately scoped/batched, and is not sitting on a path that blocks interactive or critical operations.</description>
