---
title: Graceful failure recovery
description: 'When an operation can fail partway through or encounter unexpected edge-case
  input, handle it defensively instead of letting the failure crash or leak state:'
repository: cline/cline#$(sleep 4)
label: Error Handling
language: Rust
comments_count: 3
repository_stars: 70978
---

When an operation can fail partway through or encounter unexpected edge-case input, handle it defensively instead of letting the failure crash or leak state:

1. Validate inputs that feed into arithmetic or bounds calculations (e.g., empty/inverted work areas, zero-sized regions) so the code returns a descriptive error instead of panicking. Prefer wider integer types or explicit range checks when the domain of valid inputs is larger than the happy path assumes, and cover these edge cases with regression tests.
   ```rust
   fn clamp_window_bounds(window: WindowBounds, work_area: WindowBounds) -> Result<WindowBounds, String> {
       if work_area.right <= work_area.left || work_area.bottom <= work_area.top {
           return Err("work area has zero or negative size".into());
       }
       // use i64 internally to avoid overflow/clamp(min > max) panics
       ...
   }
   ```
   On failure, log the error and fall back to a safe default (e.g., still show the window) rather than aborting setup.

2. When a multi-step operation allocates resources (spawned processes, registered sessions, open handles) and a later step fails, roll back everything already acquired before returning the error — don't leave orphaned processes or stale entries in shared state.
   ```rust
   if reader_thread_spawn_failed {
       sessions.lock().unwrap().remove(&id);
       let _ = killer.kill();
       return Err("failed to start the terminal reader".into());
   }
   ```

3. If a feature path proves unreliable or unsupported across environments (e.g., a platform API that cannot be made consistent), remove the broken path rather than leaving flaky behavior; degrade to the capability that is known to work reliably and communicate that limitation clearly to the user.

Applying these practices avoids crashes on edge-case inputs, prevents resource leaks on partial failures, and ensures the application degrades predictably when something cannot be fully supported.