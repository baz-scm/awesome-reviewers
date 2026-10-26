---
title: Timeout Bias for Safety
description: 'When a timeout is used to decide behavior based on external system state
  (IPC, DBus, network, shell/panel responsiveness), treat timeout handling as a performance
  + correctness tradeoff: keep critical threads responsive, and bias the timeout outcome
  toward the least harmful user-visible failure mode. Document the rationale and test
  the slow/ambiguous path.'
repository: cline/cline#v4
label: Performance Optimization
language: Rust
comments_count: 2
repository_stars: 70864
---

When a timeout is used to decide behavior based on external system state (IPC, DBus, network, shell/panel responsiveness), treat timeout handling as a performance + correctness tradeoff: keep critical threads responsive, and bias the timeout outcome toward the least harmful user-visible failure mode. Document the rationale and test the slow/ambiguous path.

Application:
- Don’t block a UI/main thread for probing; run the probe off-thread and wait with a bounded timeout.
- If timeout can correspond to multiple realities (e.g., “no host” vs “host present but busy”), decide which mistake is cheaper and choose that direction for the timeout result.
- Explain the tradeoff in the timeout helper’s doc/comment so future changes don’t accidentally flip the risk.
- Add a test that forces the “slow-but-present” (or equivalent) behavior.

Example pattern (Rust):
```rust
use std::{sync::mpsc, thread, time::Duration};

fn probe_with_timeout<T, E>(
    probe: impl FnOnce() -> Result<T, E> + Send + 'static,
    timeout: Duration,
    on_timeout: T, // or computed safe default
) -> T
where
    T: Send + 'static,
    E: std::fmt::Display,
{
    let (tx, rx) = mpsc::channel();
    thread::spawn(move || {
        let _ = tx.send(probe());
    });

    match rx.recv_timeout(timeout) {
        Ok(Ok(v)) => v,
        Ok(Err(_e)) => on_timeout, // treat error as equivalent to “no safe signal”
        Err(_) => on_timeout,       // timeout biases toward the safer failure mode
    }
}
```
Use comments to record *why* `on_timeout` is the safer choice for your specific failure modes.