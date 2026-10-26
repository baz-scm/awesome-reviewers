---
title: Graceful Error Recovery
description: When an operation can legitimately encounter an “already completed” or
  “invalid precondition” state at runtime, handle it as a recoverable error (or success)
  path—never as a panic.
repository: cline/cline#v5
label: Error Handling
language: Rust
comments_count: 2
repository_stars: 70864
---

When an operation can legitimately encounter an “already completed” or “invalid precondition” state at runtime, handle it as a recoverable error (or success) path—never as a panic.

Practical rules:
1) Idempotent process control: If terminating/killing a child may be called after it already exited, treat `kill()`/`wait()` outcomes accordingly and still clean up internal state so retry/respawn logic can proceed.
2) Validate inputs before panic-prone operations: Ensure preconditions are true (e.g., ranges for `clamp`) before calling APIs that can panic; if inputs are empty/inverted/out-of-range, return/log an error and degrade gracefully.
3) Make recovery testable: Add regression tests for edge cases (e.g., already-exited child handles, empty/inverted work areas, extreme coordinates).

Example pattern (process idempotency + safe cleanup):
```rust
// Treat kill-after-exit as non-fatal; always cleanup state so retry can proceed.
fn stop_child(child: &mut std::process::Child) -> Result<(), String> {
    // kill() may be Ok even if the child already exited
    let _ = child.kill();
    // wait() returns cached status if already reaped
    let _ = child.wait();
    Ok(())
}
```

Example pattern (avoid clamp panic by validating range):
```rust
fn safe_clamp(min: i32, max: i32, value: i32) -> Result<i32, String> {
    if min > max {
        return Err("invalid range".to_string());
    }
    Ok(value.clamp(min, max))
}
```

Outcome: failures become explicit, bounded, and recoverable—turning runtime edge cases into controlled error handling instead of crashes or stuck states.