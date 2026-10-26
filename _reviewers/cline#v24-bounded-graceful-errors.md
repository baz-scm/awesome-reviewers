---
title: Bounded, Graceful Errors
description: When handling failures in startup/lifecycle paths, design error handling
  to be (1) bounded, (2) non-panicking, (3) safe to log/store, and (4) aligned with
  real system API semantics.
repository: cline/cline#v24
label: Error Handling
language: Rust
comments_count: 2
repository_stars: 70891
---

When handling failures in startup/lifecycle paths, design error handling to be (1) bounded, (2) non-panicking, (3) safe to log/store, and (4) aligned with real system API semantics.

Practical rules:
- Sanitize anything you store/forward from child process logs: don’t retain sensitive startup records (tokens, auth URLs, endpoint details). Forward only sanitized output.
- Bound failure diagnostics: cap the number of stored lines and the max line length; ensure pipe-reading can’t grow memory when a process writes huge unterminated lines.
- Make recovery deterministic: time-box waits for readiness, and pace respawns with backoff so errors don’t cause tight retry loops.
- Avoid panics for recoverable inputs: validate external/platform-derived values (e.g., work area dimensions); when invalid, return an error and keep the app usable/degraded rather than crashing.
- Don’t treat “already exited” as failure: for process lifecycle calls, handle the standard behavior where kill()/wait() after reaping returns success, so retry/recovery logic proceeds correctly.

Example (pattern):
```rust
const MAX_LINES: usize = 32;
const MAX_LINE_BYTES: usize = 1024;

fn record_diagnostic(lines: &mut std::collections::VecDeque<String>, raw: &str) {
    // 1) sanitize
    let line = raw.chars()
        .filter(|c| !c.is_control())
        .take(MAX_LINE_BYTES)
        .collect::<String>();
    if line.is_empty() { return; }

    // 2) bound memory
    if lines.len() == MAX_LINES { lines.pop_front(); }
    lines.push_back(line);
}

fn graceful_ready_timeout(shutting_down: bool, endpoint: Option<String>, elapsed: std::time::Duration) -> Result<String, String> {
    if shutting_down { return Err("shutting down".into()); }
    if let Some(ep) = endpoint { return Ok(ep); }
    if elapsed > std::time::Duration::from_secs(30) {
        return Err("endpoint not published; retry startup".into());
    }
    Err("not ready".into())
}
```