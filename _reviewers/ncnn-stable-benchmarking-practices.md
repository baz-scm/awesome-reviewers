---
title: Stable Benchmarking Practices
description: When collecting performance numbers, ensure both (1) benchmark parameters
  match the target hardware and (2) the execution environment is stable/isolated—otherwise
  results can be misleading.
repository: Tencent/ncnn
label: Performance Optimization
language: Markdown
comments_count: 2
repository_stars: 23205
---

When collecting performance numbers, ensure both (1) benchmark parameters match the target hardware and (2) the execution environment is stable/isolated—otherwise results can be misleading.

Apply this:
- Use hardware-appropriate CPU threading: don’t oversubscribe a small CPU with too many threads.
- For accelerator/GPU runs, reduce sources of contention by using a conservative CPU thread count (e.g., single-thread or a value aligned to physical cores) and keep the GPU as uncontended as possible.
- If results are unstable across runs, treat it as a performance “bug” in your test setup: check whether other processes are using the GPU, stop/avoid them, and retest until the output stabilizes before updating documentation.

Example (command-line style):
- CPU thread sizing:
  - Prefer something aligned to the machine, e.g. `./benchncnn <loop> 1 ...` or `./benchncnn <loop> 8 ...` for an 8-core CPU, rather than a larger thread count.
- Retest after isolating the GPU:
  - If you suspect other GPU activity, rerun the exact same command after eliminating contention, then record only the stable run results.