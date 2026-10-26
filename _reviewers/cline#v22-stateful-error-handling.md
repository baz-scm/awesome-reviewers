---
title: Stateful error handling
description: 'When building recovery logic, don’t assume API return values map cleanly
  to “failure”. Instead, make error handling state-driven: validate inputs up front
  (to prevent panics) and use explicit process/state observations (try-wait/wait outcomes)
  to decide how to recover.'
repository: cline/cline#v22
label: Error Handling
language: Rust
comments_count: 2
repository_stars: 70886
---

When building recovery logic, don’t assume API return values map cleanly to “failure”. Instead, make error handling state-driven: validate inputs up front (to prevent panics) and use explicit process/state observations (try-wait/wait outcomes) to decide how to recover.

Apply this as two rules:
1) **Idempotent process operations aren’t “errors”.** `Child::kill()` may be `Ok(())` even if the child already exited/reaped; treat this as part of normal state transitions. Use `try_wait()`/`wait()` results to decide whether to clear/re-spawn.
2) **Validate environment/user inputs to avoid panics.** If calculations depend on external geometry or OS-provided values, guard for empty/inverted ranges and return an error (or graceful fallback) rather than letting arithmetic produce invalid clamp ranges or panicking.

Example pattern (process retry):
```rust
// Pseudocode: recovery decision must be based on observed state, not kill() alone.
if let Some(child) = process.as_mut() {
    // If already exited, kill() may still be Ok; don’t treat that as a failure.
    let exited = matches!(child.try_wait(), Ok(Some(_)));
    if exited {
        // Clear tracked state so the next step can respawn.
        *process = None;
    } else {
        // Attempt shutdown; recovery still based on subsequent state observation.
        let _ = child.kill();
        let _ = child.wait();
        *process = None;
    }
}
```

Example pattern (validation to prevent panic):
```rust
// Instead of allowing invalid clamp(min,max) ranges, detect empty/inverted work areas.
fn clamp_bounds(window: (i32,i32,i32,i32), work: (i32,i32,i32,i32)) -> Result<(i32,i32,i32,i32), String> {
    let (wl, wt, wr, wb) = work;
    let work_w = wr - wl;
    let work_h = wb - wt;
    if work_w <= 0 || work_h <= 0 {
        return Err("Invalid work area".into());
    }
    // proceed with safe clamping...
    Ok(window) // fill in real clamped values
}
```

This approach improves failure scenarios: retries don’t misclassify lifecycle semantics as errors, and UI startup doesn’t hard-crash on invalid OS/environment inputs—errors become explicit, loggable outcomes with graceful degradation.