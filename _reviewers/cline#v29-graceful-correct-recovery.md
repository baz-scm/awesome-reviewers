---
title: Graceful, correct recovery
description: 'When implementing error handling and recovery:


  1) Don’t misinterpret “success” from idempotent/late lifecycle APIs

  - Treat cleanup calls like `Child::kill()` as potentially idempotent (e.g., may
  return `Ok(())` even if the child already exited/reaped).'
repository: cline/cline#v29
label: Error Handling
language: Rust
comments_count: 2
repository_stars: 70893
---

When implementing error handling and recovery:

1) Don’t misinterpret “success” from idempotent/late lifecycle APIs
- Treat cleanup calls like `Child::kill()` as potentially idempotent (e.g., may return `Ok(())` even if the child already exited/reaped).
- Base retry/respawn decisions on actual lifecycle outcomes you observe (e.g., `try_wait`/stored state), not on the assumption that cleanup “must fail” after exit.

2) Validate preconditions and return errors instead of panicking
- For platform or external inputs, explicitly check for invalid ranges/empty/inverted values before computing/using them.
- If inputs are invalid, return a `Result` error, log the failure, and keep the app usable (degrade gracefully rather than crashing).

Practical template
```rust
fn clamp_bounds(window: Bounds, work: Bounds) -> Result<Bounds, String> {
    // Validate first (avoid invalid clamp ranges / panic paths)
    if work.right <= work.left || work.bottom <= work.top {
        return Err(format!("invalid work area: {work:?}"));
    }

    let work_width = (work.right - work.left) as i64;
    let work_height = (work.bottom - work.top) as i64;

    let width  = ((window.right - window.left) as i64)
        .max(1)
        .min(work_width);
    let height = ((window.bottom - window.top) as i64)
        .max(1)
        .min(work_height);

    let left = (window.left as i64)
        .clamp(work.left as i64, (work.right as i64) - width) as i32;
    let top = (window.top as i64)
        .clamp(work.top as i64, (work.bottom as i64) - height) as i32;

    Ok(Bounds { left, top, right: (left as i64 + width) as i32, bottom: (top as i64 + height) as i32 })
}

// Recovery example: interpret lifecycle correctly, treat kill as idempotent.
fn stop_child_and_maybe_retry(child: &mut std::process::Child) -> Result<(), String> {
    // kill may be Ok even if already exited; don’t assume failure.
    let _ = child.kill();
    let _ = child.wait(); // use returned state (or try_wait) to drive retry decisions
    Ok(())
}
```

Also: cover these paths with regression tests for edge cases (empty/inverted inputs; late/exited child handles) and make logged/returned errors specific enough to guide the next action (retry vs. permanent failure vs. safe fallback).