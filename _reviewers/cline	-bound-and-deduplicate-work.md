---
title: Bound and deduplicate work
description: Design operations to scale with the amount of actual work required, not
  with total data size, and never redo work that has already been done. When an operation
  could touch an unbounded resource (files, subprocesses, directory entries, generated
  text), impose an explicit, documented cap, and double-check that caps hold even
  when the operation is invoked...
repository: "cline/cline\t"
label: Performance Optimization
language: TypeScript
comments_count: 6
repository_stars: 70947
---

Design operations to scale with the amount of actual work required, not with total data size, and never redo work that has already been done. When an operation could touch an unbounded resource (files, subprocesses, directory entries, generated text), impose an explicit, documented cap, and double-check that caps hold even when the operation is invoked repeatedly or in batches (e.g., a per-file cap of 48k chars times 20 batched files becomes ~1M chars — consider an aggregate cap too, or confirm downstream budgets absorb it). Prefer targeted, incremental queries over full scans: fetching only the blobs for files that actually changed (`git diff --raw`) rather than listing the entire tree scales with the number of changes instead of repo size. Avoid duplicate expensive calls — if a value (a terminal snapshot, a fetched file, a rendered result) has already been computed or fetched, pass/return it and reuse it rather than re-fetching or recomputing (e.g., don't call `getLatestTerminalOutput()` twice when the fallback already captured it; don't rewrite/re-truncate a stored tool result on every subsequent request — write once at completion and reuse the stored preview/path on resume). For long-lived or growing resources (temp directories, caches), ensure there is a disposal/cleanup path so usage doesn't grow unbounded across runtime lifetime. When correctness can't be verified by mocking low-level primitives (e.g., counting spawned processes requires mocking `child_process` in ways that break promisified APIs or aren't portable), validate the fix with realistic benchmarks against production-like inputs (e.g., measuring concurrent/zombie process counts on a repo with thousands of files) instead of skipping the verification.</description>
</invoke>
