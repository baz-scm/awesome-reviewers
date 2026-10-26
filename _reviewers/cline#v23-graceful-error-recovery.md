---
title: Graceful Error Recovery
description: 'Design error handling so failures don’t crash the app and retries/stops
  remain correct under already-completed states.


  **Rules**

  1. **Turn panic conditions into handled errors + fallback.** If an invariant can
  be violated (e.g., zero/inverted geometry ranges), validate inputs before calling
  APIs that assume valid ranges. Return an error, log it, and...'
repository: cline/cline#v23
label: Error Handling
language: Rust
comments_count: 2
repository_stars: 70889
---

Design error handling so failures don’t crash the app and retries/stops remain correct under already-completed states.

**Rules**
1. **Turn panic conditions into handled errors + fallback.** If an invariant can be violated (e.g., zero/inverted geometry ranges), validate inputs before calling APIs that assume valid ranges. Return an error, log it, and degrade safely instead of panicking.
2. **Make recovery paths idempotent and terminal-state aware.** For stop/retry logic involving OS resources (processes, handles, ports), assume calls may occur after the resource already exited/reaped. Don’t treat “already done” outcomes as failures; ensure retry logic can proceed correctly when `kill()`/`wait()` return cached/benign results.

**Example (validate instead of panic)**
```rust
#[cfg(windows)]
fn clamp_bounds(window: (i32,i32,i32,i32), work: (i32,i32,i32,i32)) -> Result<(i32,i32,i32,i32), String> {
    let (wl, wt, wr, wb) = window;
    let (ml, mt, mr, mb) = work;
    if mr <= ml || mb <= mt {
        return Err("work area must be non-empty".to_string());
    }
    let work_width = mr - ml;
    let work_height = mb - mt;
    let mut width = (wr - wl).max(1).min(work_width);
    let mut height = (wb - wt).max(1).min(work_height);
    let left = wl.clamp(ml, mr - width);
    let top = wt.clamp(mt, mb - height);
    let right = left + width;
    let bottom = top + height;
    Ok((left, top, right, bottom))
}
```

**Example (retry/stop terminal-state aware)**
- When stopping a child process before respawn, treat “already exited” outcomes as success and ensure the retry path clears/updates tracked state appropriately rather than failing or double-spawning.