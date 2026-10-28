---
title: Fail gracefully, clean up state
description: 'When an operation can fail, handle it so the failure is contained and
  recoverable rather than crashing the app or leaking resources:


  1. Non-critical failures (cosmetic/positioning logic, platform-specific niceties)
  must never panic or abort startup. Validate inputs defensively (e.g., guard against
  zero-size or inverted ranges before calling `clamp`),...'
repository: cline/cline?x
label: Error Handling
language: Rust
comments_count: 3
repository_stars: 70983
---

When an operation can fail, handle it so the failure is contained and recoverable rather than crashing the app or leaking resources:

1. Non-critical failures (cosmetic/positioning logic, platform-specific niceties) must never panic or abort startup. Validate inputs defensively (e.g., guard against zero-size or inverted ranges before calling `clamp`), return a `Result`, log the failure, and fall back to a safe default so the app still launches/functions. Prefer `i64`/wider arithmetic internally when the input domain can exceed the safe range for the clamp/min/max operations you're performing.

```rust
fn clamp_window_bounds(window: WindowBounds, work_area: WindowBounds) -> Result<WindowBounds, String> {
    let work_width = work_area.right - work_area.left;
    let work_height = work_area.bottom - work_area.top;
    if work_width <= 0 || work_height <= 0 {
        return Err("empty or inverted work area".into());
    }
    // ... compute using i64 to avoid overflow, then clamp safely
}

// at the call site in setup():
match clamp_window_bounds(window, work_area) {
    Ok(bounds) => apply(bounds),
    Err(e) => log::warn!("failed to fit window: {e}"), // still reveal the window
}
```

2. When an operation acquires resources in multiple steps (spawning a process, registering a session, starting a thread), any later failure must unwind what was already allocated before the error is propagated — kill the spawned process, remove the session entry, close handles — so no orphaned processes or stale map entries survive a failed setup.

3. If a feature cannot be made reliable across all target environments (e.g., an OS API behaving inconsistently across configurations), don't ship a flaky code path with a misleading error-free success. Remove the unsupported path and narrow the documented/supported behavior to what can actually be guaranteed, rather than silently degrading or behaving inconsistently.