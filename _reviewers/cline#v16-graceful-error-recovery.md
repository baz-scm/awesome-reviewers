---
title: Graceful Error Recovery
description: Code must avoid hard crashes in critical startup/control paths. When
  things can fail (platform inputs, external processes, pipes/logs), handle errors
  by validating invariants up front, returning recoverable errors (or safe fallbacks)
  instead of panicking, and reporting failures as bounded, sanitized diagnostics.
  For recoverable external-process failures,...
repository: cline/cline#v16
label: Error Handling
language: Rust
comments_count: 2
repository_stars: 70882
---

Code must avoid hard crashes in critical startup/control paths. When things can fail (platform inputs, external processes, pipes/logs), handle errors by validating invariants up front, returning recoverable errors (or safe fallbacks) instead of panicking, and reporting failures as bounded, sanitized diagnostics. For recoverable external-process failures, use explicit timeouts plus retry/respawn backoff and make recovery loops shutdown-aware.

Practical rules:
- Validate assumptions before using operations that can panic (e.g., clamp ranges, coordinate math). If inputs are empty/inverted/invalid, return an error or fallback behavior.
- Never store or forward unbounded diagnostic output from child processes/streams; cap line length and the number of retained messages.
- Sanitize diagnostics to prevent leaking secrets (e.g., OAuth URLs/tokens/headers). Store only what you can safely display.
- Use retry logic with clear termination conditions (timeouts, “permanent” vs “retryable” failures) and pacing (backoff) to prevent crash loops.

Example (avoid panic by returning an error):
```rust
#[derive(Debug)]
struct Bounds { left: i32, top: i32, right: i32, bottom: i32 }

fn clamp_bounds(window: Bounds, work_area: Bounds) -> Result<Bounds, String> {
    if work_area.right <= work_area.left || work_area.bottom <= work_area.top {
        return Err("invalid work area bounds".to_string());
    }
    let work_w = (work_area.right - work_area.left).max(1);
    let work_h = (work_area.bottom - work_area.top).max(1);
    let width  = (window.right - window.left).max(1).min(work_w);
    let height = (window.bottom - window.top).max(1).min(work_h);

    let left = window.left.clamp(work_area.left, work_area.right - width);
    let top  = window.top.clamp(work_area.top, work_area.bottom - height);

    Ok(Bounds { left, top, right: left + width, bottom: top + height })
}

// Call site pattern: log + continue with a safe fallback instead of panicking.
```