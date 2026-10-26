---
title: Graceful, Safe Failure Handling
description: 'When handling runtime failures, ensure the system degrades gracefully
  instead of crashing, and that recovery/diagnostics are safe and predictable.


  Apply three rules:'
repository: cline/cline#v3
label: Error Handling
language: Rust
comments_count: 2
repository_stars: 70863
---

When handling runtime failures, ensure the system degrades gracefully instead of crashing, and that recovery/diagnostics are safe and predictable.

Apply three rules:
1) Prefer recoverable errors over panics for external/runtime data (e.g., OS-provided geometry). Validate before using values that can make ranges invalid, and return/record an error while keeping the app usable.
2) Treat process lifecycle actions as idempotent: `kill`/`wait`/`try_wait` may report success even if the child is already gone. Don’t infer failure from benign `Ok(())`—base retry/respawn decisions on actual state (e.g., `try_wait` outcome / tracked PID), and re-check shutdown flags.
3) Sanitize and bound any subprocess diagnostics used for user-visible errors or retries. Cap stored lines/size and omit sensitive markers.

Example pattern (input validation + safe error path):

```rust
// Validate before clamping; if invalid, return an error (no panic).
#[cfg(windows)]
fn clamp_window_bounds(window: WindowBounds, work_area: WindowBounds) -> Result<WindowBounds, String> {
    let work_left = work_area.left;
    let work_top = work_area.top;
    let work_right = work_area.right;
    let work_bottom = work_area.bottom;

    if work_right <= work_left || work_bottom <= work_top {
        return Err("invalid work area; cannot clamp window bounds".to_string());
    }

    let width = (window.right - window.left).max(1)
        .min(work_right - work_left);
    let height = (window.bottom - window.top).max(1)
        .min(work_bottom - work_top);

    let left = window.left.clamp(work_left, work_right - width);
    let top = window.top.clamp(work_top, work_bottom - height);

    Ok(WindowBounds { left, top, right: left + width, bottom: top + height })
}
```

Example pattern (idempotent process stop/retry):

```rust
// Don’t treat Ok(()) from kill as failure; re-check state instead.
let _ = child.kill(); // may be Ok even if already exited
let _ = child.wait(); // returns cached exit status
// then decide respawn based on your tracked endpoint/pid/state, not on kill() alone.
```
