---
title: Bound unbounded external output
description: When capturing or buffering output from external or long-running processes
  (child processes, hooks, wrappers, probes) whose output size is not controlled by
  your code, never let memory or disk usage grow unbounded. Enforce a fixed cap and
  keep only the relevant tail (or head) of the data, applying the most efficient mechanism
  available on each platform...
repository: can1357/oh-my-pi
label: Performance Optimization
language: JavaScript
comments_count: 4
repository_stars: 37317
---

When capturing or buffering output from external or long-running processes (child processes, hooks, wrappers, probes) whose output size is not controlled by your code, never let memory or disk usage grow unbounded. Enforce a fixed cap and keep only the relevant tail (or head) of the data, applying the most efficient mechanism available on each platform (e.g., periodic truncation plus in-memory tail, sparse-file deallocation, or piping with a bounded in-memory buffer when disk tricks aren't available). Treat this as a correctness-of-resource-usage requirement, not an afterthought: a chatty or runaway process must not be able to fill memory, fill disk, or otherwise degrade the host.

Practical guidance:
- Decide upfront the maximum bytes you are willing to retain (e.g., last 64 KiB) and design the capture/read path around that bound from the start, rather than reading/writing everything and trimming later.
- For long-running writers, poll or stream incrementally and cut data back down to the bound periodically, not only once at the end — a single untrimmed burst can still exhaust resources.
- Account for platform differences: what works on POSIX (e.g., truncating an append-mode file) may not work on Windows, and what works on NTFS (sparse files) may not work on FAT/exFAT — provide a fallback (e.g., pipe output and cap it in memory) when the primary mechanism is unavailable.
- Verify the bound empirically with a stress test: have the external process emit far more data than the cap (e.g., several MB) and assert that captured memory/disk usage stays near the bound while the retained content is still correct (e.g., ends with the process's last line).

Example pattern:
```js
const TAIL_BYTES = 64 * 1024;
const CAP_BYTES = 1024 * 1024;

// Periodically, while the process is still writing:
if (fileSize > CAP_BYTES) {
  const tail = readLastBytes(file, TAIL_BYTES);
  truncateOrDeallocateHead(file); // platform-appropriate mechanism
}
```
Apply this standard whenever reading from a subprocess, a probe command, or any stream whose size is determined by code outside your control.