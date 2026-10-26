---
title: Bounded Graceful Error Handling
description: When handling errors or uncertain runtime states, design behavior that
  is (1) bounded, (2) safe-by-default, (3) diagnostic-but-not-sensitive, and (4) recoverable
  without panics.
repository: cline/cline#x
label: Error Handling
language: Rust
comments_count: 3
repository_stars: 70861
---

When handling errors or uncertain runtime states, design behavior that is (1) bounded, (2) safe-by-default, (3) diagnostic-but-not-sensitive, and (4) recoverable without panics.

Apply this standard:
- Decide the “cheaper mistake” for ambiguous timeouts/probes. Document why and bias toward the outcome that avoids breaking user sessions or leaving the app stuck.
- Keep critical threads responsive: any probe/wait must have a hard timeout and should not stall UI/main threads.
- Make diagnostics safe and bounded:
  - sanitize/redact sensitive content before storing/forwarding;
  - cap number/size of buffered diagnostic lines to prevent unbounded memory growth;
  - include only actionable context in error messages (what failed + what to try).
- Recover deterministically:
  - serialize startup/retries with clear lock ordering;
  - re-check shutdown state under locks to avoid spawning after teardown;
  - respawn only when appropriate, using backoff/spacing to avoid crash loops;
  - handle retry cases where processes may already have exited.
- Prefer graceful degradation over panics for runtime inputs. Validate early; on invalid/unexpected environment data, return an error, log it, and fall back to a usable experience.

Example pattern (bounded, safe default with actionable recovery):
```rust
const TIMEOUT: Duration = Duration::from_millis(250);
fn probe_safely() -> bool {
    // Run probe off the main thread.
    let (tx, rx) = std::sync::mpsc::channel();
    std::thread::spawn(move || { let _ = tx.send(run_probe()); });

    match rx.recv_timeout(TIMEOUT) {
        // If ambiguous, resolve toward the safer user-visible outcome.
        Ok(Ok(registered)) => registered,
        Ok(Err(_reason)) | Err(std::sync::mpsc::RecvTimeoutError::Timeout) => {
            // Safe-by-default: degrade rather than risk a stuck running session.
            false
        }
        Err(_) => false,
    }
}
```

This standard directly targets the recurring pitfalls shown in the discussions: ambiguous timeouts chosen without user-safety reasoning, unbounded diagnostics, blocking waits, racy retry behavior, and panics on invalid runtime environment data.