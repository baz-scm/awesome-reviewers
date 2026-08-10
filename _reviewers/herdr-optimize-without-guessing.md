---
title: Optimize Without Guessing
description: When performance-critical code interacts with OS/process state or remote
  services, optimize by reducing unnecessary work *only when correctness is preserved*.
repository: ogulcancelik/herdr
label: Performance Optimization
language: Rust
comments_count: 2
repository_stars: 26924
---

When performance-critical code interacts with OS/process state or remote services, optimize by reducing unnecessary work *only when correctness is preserved*.

Apply:
1) Gate expensive scans behind capability probes, and cache the probe result once per process.
   - Example pattern:
   ```rust
   fn feature_supported() -> bool {
       static SUPPORTED: std::sync::OnceLock<bool> = std::sync::OnceLock::new();
       *SUPPORTED.get_or_init(|| {
           std::fs::metadata("/some/feature/file").is_ok()
       })
   }
   ```
2) Prefer streaming enumeration over materializing large collections when you’re going to inspect every candidate anyway.
   - Example pattern:
   ```rust
   fn all_ids_streaming() -> impl Iterator<Item=u32> {
       std::fs::read_dir("/proc")
           .into_iter()
           .flatten()
           .flatten()
           .filter_map(|e| numeric_file_name(&e))
   }
   ```
3) If you introduce limits, define the “fail-closed” behavior precisely (including off-by-one), and unit-test the bound + filtering logic. Don’t cap using iteration order when you don’t have an index to ensure correctness.
   - Rule of thumb: only truncate when you can prove the truncation can’t skip a needed match.
4) Don’t cache or skip per-operation safety checks (e.g., protocol compatibility) if the cached view can become stale between operations. If performance matters, optimize via better dispatch/negotiation on the same connection rather than weakening validation.

Net effect: you cut work (gating/streaming) without introducing silent correctness regressions (unsafe caps/order reliance) or stale-server hazards (unsafe caching).