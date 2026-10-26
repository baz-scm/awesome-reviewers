---
title: Deterministic, Safe Error Handling
description: Implement error handling that (1) fails deterministically under ambiguity,
  (2) retries/recovers with bounded time and backoff, (3) never panics on recoverable
  runtime/environment failures, and (4) treats diagnostics as sensitive and bounded.
repository: cline/cline#v13
label: Error Handling
language: Rust
comments_count: 3
repository_stars: 70874
---

Implement error handling that (1) fails deterministically under ambiguity, (2) retries/recovers with bounded time and backoff, (3) never panics on recoverable runtime/environment failures, and (4) treats diagnostics as sensitive and bounded.

How to apply:
- Timeout/probe ambiguity: when “missing vs slow” is indistinguishable, explicitly bias toward the safer failure mode and document why.
  - Prefer: `recv_timeout` + fallback state.
- Bounded recovery: for sidecars/IPC/process readiness, cap diagnostics memory, cap/pace retries (`poll_interval`, `respawn_backoff`), and ensure state changes only apply to the currently-tracked process.
- Safe diagnostics: sanitize logs/errors to avoid tokens/URLs, and bound handling for huge/unterminated lines.
- No panics for environment/runtime: validate preconditions; return an error and degrade gracefully (e.g., still reveal the window) rather than crashing.

Example pattern (timeout with deterministic fallback + safe diagnostics):
```rust
fn probe_with_timeout(timeout: Duration) -> bool {
    let (tx, rx) = std::sync::mpsc::channel();
    std::thread::spawn(move || {
        let ok = /* read/inspect external state */ true;
        let _ = tx.send(ok);
    });
    match rx.recv_timeout(timeout) {
        Ok(registered) => registered,
        Err(_) => {
            // Deterministic fallback: choose the safer behavior.
            // (e.g., hide rather than quitting, or vice versa—document it.)
            false
        }
    }
}

fn sanitize_diagnostic(line: &str) -> String {
    // Strip/omit sensitive markers and cap size.
    let capped: String = line.chars().filter(|c| !c.is_control()).take(1024).collect();
    capped
}
```