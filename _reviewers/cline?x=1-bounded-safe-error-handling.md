---
title: Bounded, Safe Error Handling
description: When handling failures, make the behavior under error/timeout explicit,
  keep critical threads responsive, and provide bounded, safe recovery plus sanitized
  diagnostics.
repository: cline/cline?x=1
label: Error Handling
language: Rust
comments_count: 3
repository_stars: 70861
---

When handling failures, make the behavior under error/timeout explicit, keep critical threads responsive, and provide bounded, safe recovery plus sanitized diagnostics.

Practical rules:
1) Bias ambiguous timeouts intentionally
- If you must time out, choose which direction is safer (e.g., “prefer hide over quit” when unsure) and document the rationale.
- Ensure timeouts protect UI/main threads from blocking.

2) Use bounded recovery loops
- For retry/respawn paths, cap wait times, add backoff to avoid crash-loops, and serialize access with clear lock ordering.
- Prevent orphaned subprocesses and racey state by rechecking shutdown/ownership (e.g., only clear endpoint if the PID still matches).

3) Make diagnostics safe and bounded
- Don’t store or forward potentially sensitive logs; sanitize before buffering/returning.
- Bound memory growth (max lines, max line length) and still drain stdout/stderr so failures can’t wedge the process.

4) Prefer graceful degradation over panics
- Validate platform-/environment-dependent inputs early (e.g., geometry/work area). Return errors that trigger fallback behavior rather than panicking.
- Add regression tests for edge-case inputs (empty/inverted ranges, extreme coordinates).

Example pattern (timeout with deliberate bias + non-blocking main thread):
```rust
use std::{sync::mpsc, thread, time::Duration};

fn probe_with_timeout(probe: impl FnOnce() -> Result<bool, String> + Send + 'static,
                      timeout: Duration) -> bool {
    // Offload so the caller thread (often UI) never stalls.
    let (tx, rx) = mpsc::channel();
    thread::spawn(move || { let _ = tx.send(probe()); });

    match rx.recv_timeout(timeout) {
        Ok(Ok(registered)) => registered,
        Ok(Err(_reason)) => {
            // Intentionally biased fallback: choose the least harmful state.
            false
        }
        Err(_timeout) => {
            // Documented bias for ambiguous failures.
            false
        }
    }
}
```
Adopt this as a team standard for startup, subprocess lifecycle, UI-triggered operations, and any environment-dependent logic.