---
title: Idempotent Recovery and Validation
description: In error handling and recovery paths, design for (1) idempotent operations
  and (2) invalid-input resilience—avoid panics and recover without blocking forward
  progress.
repository: cline/cline#v4
label: Error Handling
language: Rust
comments_count: 2
repository_stars: 70864
---

In error handling and recovery paths, design for (1) idempotent operations and (2) invalid-input resilience—avoid panics and recover without blocking forward progress.

Key rules:
- Idempotent “already finished” outcomes are not failures: when stopping/reaping processes or performing cleanup, treat cases like “kill after exit” as success. Use state queries (e.g., `try_wait`, readiness flags) to decide whether to respawn, rather than assuming kill/wait errors indicate a real problem.
- Validate preconditions for range math and clamping: before calling `clamp(min, max)` (or any function that assumes ordering), explicitly detect empty/inverted ranges and return an error.
- Prefer graceful degradation over panic: for invalid environment/state (e.g., zero/inverted work area), return a structured error, log it, and continue with a safe fallback.

Example: idempotent process stop/recovery
```rust
fn stop_child_and_maybe_respawn(child: &mut std::process::Child) -> Result<(), String> {
    // Kill is allowed to be Ok even if the process already exited.
    let _ = child.kill();

    // wait() may return cached status even if already reaped.
    let _status = child
        .wait()
        .map_err(|e| format!("failed to wait for child: {e}"))?;

    Ok(())
}
```

Example: validate clamp inputs and degrade gracefully
```rust
#[derive(Clone, Copy, Debug)]
struct Bounds { left: i32, top: i32, right: i32, bottom: i32 }

fn clamp_bounds_or_error(window: Bounds, work: Bounds) -> Result<Bounds, String> {
    if work.right <= work.left || work.bottom <= work.top {
        return Err("work area is empty or inverted".to_string());
    }
    let work_w = work.right - work.left;
    let work_h = work.bottom - work.top;
    let w = (window.right - window.left).clamp(1, work_w);
    let h = (window.bottom - window.top).clamp(1, work_h);
    let left = window.left.clamp(work.left, work.right - w);
    let top = window.top.clamp(work.top, work.bottom - h);
    Ok(Bounds { left, top, right: left + w, bottom: top + h })
}

// Call site should log and continue with a safe fallback rather than panic.
```