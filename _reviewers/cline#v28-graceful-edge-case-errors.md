---
title: Graceful Edge-Case Errors
description: 'Handle errors and edge cases explicitly—avoid panics, and don’t treat
  idempotent “already finished” operations as failures.


  **How to apply**

  1. **Validate preconditions before arithmetic/clamping.** If environment inputs
  can be empty/inverted/zero-sized, either return an error or fall back to a safe
  behavior (e.g., still show the window) and log it.'
repository: cline/cline#v28
label: Error Handling
language: Rust
comments_count: 2
repository_stars: 70893
---

Handle errors and edge cases explicitly—avoid panics, and don’t treat idempotent “already finished” operations as failures.

**How to apply**
1. **Validate preconditions before arithmetic/clamping.** If environment inputs can be empty/inverted/zero-sized, either return an error or fall back to a safe behavior (e.g., still show the window) and log it.
2. **Drive retries/cleanup from authoritative state.** For external resources (processes, files, ports), assume teardown may be a no-op if the resource already terminated. Structure logic around `try_wait`/readiness state, and only retry/respawn when it’s truly needed.
3. **Add regression tests for boundary conditions.** Include empty/inverted/degenerate inputs and state-transition scenarios.

**Example (process retry/teardown pattern)**
```rust
match child.try_wait() {
    Ok(Some(_status)) => {
        // Child is already reaped/finished: treat kill/wait as non-fatal.
        let _ = child.kill(); // may be Ok even if already exited
        let _ = child.wait(); // cached status is fine
        *process = None;
    }
    Ok(None) => {
        // Still running: attempt shutdown then wait/reap.
        let _ = child.kill();
        let _ = child.wait();
        *process = None;
    }
    Err(e) => {
        // Only now do you propagate/escalate.
        return Err(format!("failed to check child state: {e}"));
    }
}
```

This standard improves **Error Handling** by making failures recoverable, avoiding crash-on-invalid-input behavior, and making retry logic correct under real asynchronous state transitions.