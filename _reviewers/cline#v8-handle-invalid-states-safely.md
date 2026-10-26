---
title: Handle invalid states safely
description: 'When implementing startup/retry logic or range computations, treat “invalid
  state” as a first-class error path: validate preconditions to avoid panics, and
  interpret OS/process results conservatively so retries don’t misbehave.'
repository: cline/cline#v8
label: Error Handling
language: Rust
comments_count: 2
repository_stars: 70867
---

When implementing startup/retry logic or range computations, treat “invalid state” as a first-class error path: validate preconditions to avoid panics, and interpret OS/process results conservatively so retries don’t misbehave.

Apply:
1) Validate derived values before calling functions that assume well-formed ranges.
   - If work areas/ranges can be empty or inverted, return an error (log + degrade gracefully) instead of relying on arithmetic guards that could still lead to panics.
2) Make process control code resilient to idempotent outcomes.
   - `Child::kill()` / `wait()` may return `Ok` even if the child already exited; don’t treat that as “still running” or “retry should not proceed”. Update cached state based on actual liveness (e.g., `try_wait`) and ensure retry/respawn decisions are consistent.

Example pattern (Rust-style):
```rust
fn safe_clamp_window_bounds(window: (i32,i32,i32,i32), work: (i32,i32,i32,i32))
    -> Result<(i32,i32,i32,i32), String>
{
    let (wl, wt, wr, wb) = work;
    let work_w = (wr - wl) as i64;
    let work_h = (wb - wt) as i64;
    if work_w <= 0 || work_h <= 0 {
        return Err("work area is empty or inverted".to_string());
    }

    // Use i64 to avoid overflow, then clamp back to i32.
    let (x1,y1,x2,y2) = window;
    let w = (x2 - x1) as i64;
    let h = (y2 - y1) as i64;
    let width  = w.max(1).min(work_w) ;
    let height = h.max(1).min(work_h);

    let left = (x1 as i64).clamp(wl as i64, (wr as i64) - width) as i32;
    let top  = (y1 as i64).clamp(wt as i64, (wb as i64) - height) as i32;
    Ok((left, top, left + width as i32, top + height as i32))
}
```

For sidecar/process retries: base respawn/state transitions on liveness checks (`try_wait`/stored PID identity), and treat “Ok” from `kill()`/`wait()` as potentially meaning “already exited”—then clear/recreate state deterministically and continue controlled recovery rather than failing or looping incorrectly.