---
title: Graceful Error Degradation
description: 'Handle edge-case and expected failure modes as *recoverable* instead
  of causing crashes or uncontrolled behavior. Concretely:


  - **Avoid panics in startup/UI paths**: validate preconditions and return a recoverable
  error (log + continue with safe fallback) rather than letting functions panic.'
repository: cline/cline#v10
label: Error Handling
language: Rust
comments_count: 2
repository_stars: 70869
---

Handle edge-case and expected failure modes as *recoverable* instead of causing crashes or uncontrolled behavior. Concretely:

- **Avoid panics in startup/UI paths**: validate preconditions and return a recoverable error (log + continue with safe fallback) rather than letting functions panic.
- **Treat “already happened” OS/process outcomes as non-fatal**: e.g., if a child has already exited, `kill()`/`wait()` should not be escalated into a failed retry—let the state machine progress (e.g., clear/reap and optionally respawn).
- **Make failure reporting safe and bounded**: sanitize diagnostics to avoid leaking sensitive data, and bound memory/line lengths when reading/recording log output.
- **Keep recovery deterministic**: retries should be paced and should not spawn duplicate processes due to races.

Example pattern (validation + recoverable fallback):
```rust
// Instead of panicking on invalid environment, return an error and continue.
fn try_clamp_window_bounds(window: WindowBounds, work_area: WindowBounds) -> Result<WindowBounds, String> {
    let work_w = work_area.right - work_area.left;
    let work_h = work_area.bottom - work_area.top;
    if work_w <= 0 || work_h <= 0 {
        return Err("work area is empty/inverted".to_string());
    }
    // ... safe clamping math ...
    Ok(window)
}

// Call site: log failure and continue (no panic).
match try_clamp_window_bounds(window, work_area) {
    Ok(b) => apply_bounds(b),
    Err(e) => {
        log::warn!("window fitting failed: {e}");
        reveal_window();
    }
}
```

Example pattern (process lifecycle):
```rust
// If the child is already gone, treat kill/wait as non-fatal and progress state.
if let Some(child) = process.as_mut() {
    // kill() may return Ok(()) even after exit; don’t treat as a hard error.
    let _ = child.kill();
    let _ = child.wait(); // reaps cached status
    *process = None; // advance state machine
    // optionally respawn on next step
}
```