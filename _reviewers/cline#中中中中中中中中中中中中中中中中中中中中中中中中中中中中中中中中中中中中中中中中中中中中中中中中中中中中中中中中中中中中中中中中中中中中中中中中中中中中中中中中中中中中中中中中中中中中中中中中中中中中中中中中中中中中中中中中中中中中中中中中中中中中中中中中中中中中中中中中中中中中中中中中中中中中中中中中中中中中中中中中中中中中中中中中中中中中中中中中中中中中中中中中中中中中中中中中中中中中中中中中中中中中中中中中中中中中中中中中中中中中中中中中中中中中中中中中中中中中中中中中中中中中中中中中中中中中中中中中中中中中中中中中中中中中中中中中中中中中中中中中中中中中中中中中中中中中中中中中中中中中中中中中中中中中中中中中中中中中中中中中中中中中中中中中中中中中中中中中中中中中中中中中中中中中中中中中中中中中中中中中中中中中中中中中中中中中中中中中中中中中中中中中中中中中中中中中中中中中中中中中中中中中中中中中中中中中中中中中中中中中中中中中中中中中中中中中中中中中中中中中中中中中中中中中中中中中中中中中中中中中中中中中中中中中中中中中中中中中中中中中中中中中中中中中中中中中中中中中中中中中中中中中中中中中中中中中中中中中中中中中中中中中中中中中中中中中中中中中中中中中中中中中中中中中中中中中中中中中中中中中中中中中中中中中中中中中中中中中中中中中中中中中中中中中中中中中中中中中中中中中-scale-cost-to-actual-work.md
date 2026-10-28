---
title: Scale cost to actual work
description: Design operations so their cost scales with the amount of work actually
  required, not with the size of the whole repository, dataset, or an unrelated upper
  bound — and never pay for the same expensive operation twice. Before adding a loop,
  fetch, or subprocess spawn per item, ask whether it can be scoped to only the changed/needed
  subset, batched into a...
repository: cline/cline#中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中
label: Performance Optimization
language: TypeScript
comments_count: 6
repository_stars: 70984
---

Design operations so their cost scales with the amount of work actually required, not with the size of the whole repository, dataset, or an unrelated upper bound — and never pay for the same expensive operation twice. Before adding a loop, fetch, or subprocess spawn per item, ask whether it can be scoped to only the changed/needed subset, batched into a single call, or cached/reused across call sites.

Concretely:
- Scope expensive I/O (network fetches, full-tree walks) to only what the task needs. For example, prefer `git diff --raw` against changed paths over a full `git ls-tree -r` of the whole repository, and avoid fetching remote history before it's confirmed to be needed.
- Batch repeated subprocess/API calls instead of spawning one process per file or item (e.g., a single `git cat-file --batch` instead of one `git show` per file); uncontrolled per-item spawning can produce thousands of concurrent processes on large inputs.
- Never call the same expensive function twice to get the same result. If a helper already computed a value needed elsewhere (e.g., a terminal snapshot, a fetched blob), return or cache that value and reuse it rather than re-invoking the expensive path.
- When applying size/count caps to bound resource usage, account for multiplicative effects (e.g., a per-item cap multiplied by the number of items can still produce an unbounded aggregate) and cap the aggregate where relevant.
- When you intentionally keep a bounded but non-trivial cost (e.g., synchronous reads capped at N files of M bytes, or holding all results in memory rather than streaming), document the bound and the reasoning so reviewers and future maintainers can evaluate the trade-off, and validate assumptions with realistic benchmarks (e.g., process counts measured against large real-world repos) rather than guesses.