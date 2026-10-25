---
title: Timeouts With Safe Bias
description: When adding timeouts around external/IPC checks (especially those triggered
  from UI/closing handlers), ensure you both bound execution time *and* choose a timeout
  fallback that favors the lowest-impact, most likely failure.
repository: CLINE/CLINE
label: Performance Optimization
language: Rust
comments_count: 2
repository_stars: 70837
---

When adding timeouts around external/IPC checks (especially those triggered from UI/closing handlers), ensure you both bound execution time *and* choose a timeout fallback that favors the lowest-impact, most likely failure.

Apply this standard:
- **Don’t stall the UI thread**: move the probe to a background thread and enforce a **small timeout**.
- **Make the timeout deterministic**: if the timeout can represent multiple real states, explicitly decide which behavior is safer.
- **Bias toward the cheaper failure mode**: prefer the fallback that avoids catastrophic side effects when “host present but slow” is more plausible than “host missing but stalled.”
- **Avoid unnecessary waits on guaranteed-fail paths**: rely on immediate connection/lookup failures (e.g., missing bus/watchers) so the timeout is only reached for truly slow-but-present services.
- **Document and test the reasoning**: record why the fallback direction was chosen and add coverage for the slow-probe path.

Example pattern:
```rust
use std::{sync::mpsc, thread, time::Duration};

fn probe_with_safe_timeout<F>(probe: F, timeout: Duration) -> bool
where
    F: FnOnce() -> bool + Send + 'static,
{
    let (tx, rx) = mpsc::channel();
    thread::spawn(move || { let _ = tx.send(probe()); });

    // Timeout fallback should be biased toward the safer behavior,
    // not just “whichever state seems likely.”
    match rx.recv_timeout(timeout) {
        Ok(registered) => registered,
        Err(_) => {
            // e.g., treat as present or absent depending on impact/likelihood.
            false
        }
    }
}
```
Use a short timeout and a documented, intentionally chosen fallback so performance doesn’t degrade user experience and the system behaves predictably under ambiguity.