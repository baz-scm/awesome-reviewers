---
title: Graceful Failure Defaults
description: 'When interacting with external systems or edge-case inputs, design error
  handling so the app stays usable: (1) use bounded waits and a deterministic safe
  default when you can’t reliably determine state, and (2) validate inputs and return
  recoverable errors instead of panicking.'
repository: cline/cline#v20
label: Error Handling
language: Rust
comments_count: 2
repository_stars: 70886
---

When interacting with external systems or edge-case inputs, design error handling so the app stays usable: (1) use bounded waits and a deterministic safe default when you can’t reliably determine state, and (2) validate inputs and return recoverable errors instead of panicking.

Practical rules:
- Bound potentially blocking operations (especially on UI/main threads). Use a short timeout and decide what to do if the result can’t be obtained in time.
- If the timeout/absence is ambiguous, explicitly document which failure direction is cheaper and intentionally bias toward that outcome.
- Prefer “no crash” semantics for invalid/edge inputs: detect empty/inverted/unsupported conditions early, return an error (Result), and degrade gracefully (e.g., log and keep the UI usable).
- Add regression tests for the ambiguous cases (timeout/slow responders) and the edge inputs (empty/extreme coordinates).

Example pattern:
```rust
use std::{thread, time::Duration, sync::mpsc};

fn try_check_with_timeout<F>(probe: F, timeout: Duration) -> bool
where
    F: FnOnce() -> Result<bool, String> + Send + 'static,
{
    // Bound blocking work; decide a safe default under ambiguity.
    let (tx, rx) = mpsc::channel();
    thread::spawn(move || { let _ = tx.send(probe()); });

    match rx.recv_timeout(timeout) {
        Ok(Ok(v)) => v,
        Ok(Err(reason)) => {
            eprintln!("probe failed: {reason}");
            false // documented safe default
        }
        Err(_) => {
            // Timeout: choose the cheaper mistake and return a deterministic value.
            false // e.g., “avoid quitting / hide” style safe behavior
        }
    }
}

fn clamp_bounds_safe(work_width: i32) -> Result<i32, String> {
    if work_width <= 0 {
        return Err("work area must be non-empty".into());
    }
    Ok(work_width)
}
```
Applying this reduces “invisible failure” modes (timeouts that hang or ambiguous environmental state) and “hard failure” modes (panics on edge inputs).