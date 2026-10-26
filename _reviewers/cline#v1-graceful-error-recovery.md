---
title: Graceful Error Recovery
description: 'When handling runtime failures (especially platform inputs and external
  processes), make error paths predictable and non-panicking: validate preconditions
  up front, treat lifecycle/“already exited” outcomes as non-fatal, and surface failures
  with safe, bounded diagnostics.'
repository: cline/cline#v1
label: Error Handling
language: Rust
comments_count: 2
repository_stars: 70862
---

When handling runtime failures (especially platform inputs and external processes), make error paths predictable and non-panicking: validate preconditions up front, treat lifecycle/“already exited” outcomes as non-fatal, and surface failures with safe, bounded diagnostics.

**Do**
- **Avoid panics from dynamic inputs**: check invariants (e.g., non-empty clamp ranges) and return a recoverable `Result`/error instead of panicking.
- **Make external recovery idempotent**: if a process may have already exited, treat `kill()`/stop attempts as best-effort and proceed with cleanup + retry logic.
- **Keep failure reporting safe**: sanitize or redact sensitive output, bound memory while reading logs/diagnostics, and convert internal errors into clear user-facing retry guidance.

**Don’t**
- Don’t let platform edge cases (zero-sized/inverted areas, unexpected coordinate ranges) panic the app—fail gracefully.
- Don’t treat “already done” lifecycle states (e.g., kill after exit) as hard failures that block recovery.

**Example patterns**
```rust
// 1) External process: make stop/retry idempotent
fn stop_child_best_effort(child: &mut std::process::Child) -> Result<(), String> {
    // In modern Rust std, kill() after the child already exited is treated as Ok.
    // Treat it as non-fatal; always attempt wait/reap.
    let _ = child.kill().map_err(|e| format!("kill failed: {e}"));
    let _ = child.wait().map_err(|e| format!("wait failed: {e}"));
    Ok(())
}

// 2) Platform input: avoid panic from invalid clamp ranges
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
struct WindowBounds { left: i32, top: i32, right: i32, bottom: i32 }

fn clamp_window_bounds_checked(
    window: WindowBounds,
    work_area: WindowBounds,
) -> Result<WindowBounds, String> {
    let work_w = work_area.right - work_area.left;
    let work_h = work_area.bottom - work_area.top;
    if work_w <= 0 || work_h <= 0 {
        return Err("work area is empty or inverted".to_string());
    }
    let width = (window.right - window.left).max(1).min(work_w);
    let height = (window.bottom - window.top).max(1).min(work_h);
    let left = window.left.clamp(work_area.left, work_area.right - width);
    let top = window.top.clamp(work_area.top, work_area.bottom - height);
    Ok(WindowBounds { left, top, right: left + width, bottom: top + height })
}
```

Applying this standard reduces crash risk, improves reliability under retries, and ensures failures are diagnosable without leaking sensitive or unbounded output.