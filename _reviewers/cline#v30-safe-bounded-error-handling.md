---
title: Safe, Bounded Error Handling
description: When failures are possible (external processes, readiness waits, OS/window
  metrics, parsing), design error handling to be (1) safe (no sensitive data leakage),
  (2) bounded (no unbounded memory/loops), (3) panic-free (validate inputs and return
  `Result`/error paths), and (4) recoverable with clear user/actionable messaging
  (timeouts/backoff for retries).
repository: cline/cline#v30
label: Error Handling
language: Rust
comments_count: 2
repository_stars: 70894
---

When failures are possible (external processes, readiness waits, OS/window metrics, parsing), design error handling to be (1) safe (no sensitive data leakage), (2) bounded (no unbounded memory/loops), (3) panic-free (validate inputs and return `Result`/error paths), and (4) recoverable with clear user/actionable messaging (timeouts/backoff for retries).

Apply this as team standards:
- Sanitize and limit diagnostics: never persist/replay sensitive strings from subprocess output; cap line length and number of stored diagnostics; keep draining output pipes even if the sink fails.
- Make recovery bounded: any retry/wait loop must have a deadline and backoff (and record the last relevant failure/exit info for debugging).
- Avoid panics from assumptions: if environment-derived values (like work-area geometry) can be empty/inverted/degenerate, treat it as an error and degrade gracefully (log + continue with a safe fallback), backed by tests.

Example pattern (sanitized, bounded, retrying readiness):
```rust
// 1) Validate to avoid panics
fn clamp_range(x: i32, min: i32, max: i32) -> Result<i32, String> {
    if min > max { return Err("invalid range".into()); }
    Ok(x.clamp(min, max))
}

// 2) Sanitize/bound subprocess diagnostics
fn sanitize_line(s: &str) -> String {
    const MAX: usize = 512;
    let filtered: String = s.chars().filter(|c| !c.is_control()).take(MAX).collect();
    filtered // plus marker-based redaction in real code
}

// 3) Bounded wait + retry with backoff + actionable error
fn wait_with_retry<F: FnMut() -> Result<(), String>>(deadline: std::time::Instant, mut respawn: F) -> Result<(), String> {
    let mut backoff_ms = 200u64;
    while std::time::Instant::now() < deadline {
        // check readiness here...
        // if readiness failed and child exited: respawn()
        respawn()?; // respawn should be paced by backoff
        std::thread::sleep(std::time::Duration::from_millis(backoff_ms));
        backoff_ms = (backoff_ms * 2).min(2000);
    }
    Err("component did not become ready within the deadline; retry startup".into())
}
```