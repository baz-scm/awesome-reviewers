---
title: Graceful failure handling
description: When an operation can fail at runtime—especially on edge-case inputs
  or platform-specific behavior—prefer returning a descriptive `Result`/error over
  letting the code panic or silently leave the system in an inconsistent state. Before
  propagating an error, fully clean up any partially-created resources (threads, handles,
  map entries, spawned processes) so...
repository: cline/cline#1
label: Error Handling
language: Rust
comments_count: 3
repository_stars: 71024
---

When an operation can fail at runtime—especially on edge-case inputs or platform-specific behavior—prefer returning a descriptive `Result`/error over letting the code panic or silently leave the system in an inconsistent state. Before propagating an error, fully clean up any partially-created resources (threads, handles, map entries, spawned processes) so failures don't leak state. Also validate inputs that feed into operations which can panic on malformed data (e.g., `clamp(min, max)` with an inverted range from a zero-size or corrupted work area) and return an error instead of crashing, allowing the caller to log the failure and continue in a degraded-but-functional mode rather than aborting entirely.

If a feature or code path cannot be made reliable across all target environments (e.g., an OS API that only works inconsistently), don't keep a fragile "best effort" implementation that silently fails—remove it and scope the feature down to what is demonstrably supported, with clear documentation of the limitation.

Example pattern:

```rust
fn clamp_window_bounds(window: Bounds, work_area: Bounds) -> Result<Bounds, String> {
    let work_width = work_area.right - work_area.left;
    let work_height = work_area.bottom - work_area.top;
    if work_width <= 0 || work_height <= 0 {
        return Err("work area has zero or negative size".into());
    }
    // ... safe clamping using i64 to avoid overflow
    Ok(clamped)
}

// On spawn failure, clean up before returning the error:
if thread_spawn_failed {
    sessions.lock().unwrap().remove(&id);
    let _ = killer.kill();
    return Err("failed to start the terminal reader".into());
}
```

Applying this consistently prevents crashes on unexpected inputs, avoids orphaned resources/processes after partial failures, and ensures user-facing behavior degrades gracefully instead of hard-failing.