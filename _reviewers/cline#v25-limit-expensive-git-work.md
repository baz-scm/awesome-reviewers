---
title: Limit Expensive Git Work
description: 'Standardize performance around expensive external/process and repo-scope
  operations:


  1) **Scope git/network enumeration**: don’t fetch/compute over *all* remote heads/branches
  by default. Prefer upstream/default branch, a bounded ref set, or local tracking
  refs.'
repository: cline/cline#v25
label: Performance Optimization
language: TypeScript
comments_count: 4
repository_stars: 70891
---

Standardize performance around expensive external/process and repo-scope operations:

1) **Scope git/network enumeration**: don’t fetch/compute over *all* remote heads/branches by default. Prefer upstream/default branch, a bounded ref set, or local tracking refs.
2) **Batch process-heavy git reads**: when you need many blobs/files, use a single git process (e.g., `git cat-file --batch`) rather than spawning one per file.
3) **Cap output and buffer sizes**: enforce strict `timeout`/`maxBuffer`/archive-size limits; skip large blobs when appropriate.
4) **Deduplicate snapshot/capture calls**: if a call already fetches a snapshot, reuse it for both downstream messaging and telemetry—never call the capture twice.
5) **Degrade gracefully to partial data**: when caps/timeouts are reached, return a `{ state: "partial" }` (or equivalent) rather than failing or discarding all results.

Example (dedupe telemetry snapshot):
```ts
// Fetch terminal snapshot once and reuse it for both fallback messaging and telemetry.
const terminalSnapshot = await getLatestTerminalOutput();
await returnCurrentTerminalContents(terminalSnapshot);
telemetryService.captureTerminalOutputFailure(reason, {
  snapshot: terminalSnapshot,
});
```

Apply the same mindset to remote enumeration and git status reads: keep the ref set small, the batch size bounded, and ensure limit breaches still produce useful (partial) output.