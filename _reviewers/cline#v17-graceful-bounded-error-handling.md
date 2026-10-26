---
title: Graceful bounded error handling
description: When code can fail (invalid inputs, startup/IPC readiness, subprocess
  lifecycle), handle failures deterministically and safely—avoid panics, cap/bound
  diagnostics, and return/log actionable errors.
repository: cline/cline#v17
label: Error Handling
language: Rust
comments_count: 2
repository_stars: 70883
---

When code can fail (invalid inputs, startup/IPC readiness, subprocess lifecycle), handle failures deterministically and safely—avoid panics, cap/bound diagnostics, and return/log actionable errors.

Apply these rules:
- No panics from expected edge cases: validate inputs (e.g., empty/inverted system-provided ranges) and convert them into handled failures that don’t crash the app.
- Sanitize and bound any diagnostic captured during failures: never retain/replay sensitive content; cap log line length and the number of buffered diagnostic lines.
- Use explicit timeouts + bounded retry/backoff for recovery: wait for readiness with a deadline, then return a clear error; respawn retries should be paced to prevent crash loops.
- Ensure error messages describe what failed and what the user/system should do next (e.g., “Retry startup” plus bounded diagnostic context).

Example pattern (Rust-like):
```rust
const MAX_LINES: usize = 32;
const MAX_LINE_LEN: usize = 1024;

fn sanitize(line: &str) -> String {
    // redact/omit sensitive markers
    let line = line.trim();
    line.chars().filter(|c| !c.is_control()).take(MAX_LINE_LEN).collect()
}

fn record_failure(diagnostics: &mut Vec<String>, line: &str) {
    if diagnostics.len() == MAX_LINES {
        diagnostics.remove(0);
    }
    let s = sanitize(line);
    if !s.is_empty() {
        diagnostics.push(s);
    }
}

fn wait_with_timeout_and_retry<F>(deadline: std::time::Instant, mut retry: F) -> Result<String, String>
where
    F: FnMut() -> Result<(), String>,
{
    let mut backoff = std::time::Duration::from_secs(2);
    while std::time::Instant::now() < deadline {
        // check readiness...
        // if failed and child exited -> retry() with pacing
        // std::thread::sleep(poll_interval);
        // backoff += ... (optional)
    }
    retry().map_err(|e| e)?;
    Err("Did not publish endpoint within timeout; retry startup".to_string())
}
```
Use tests for boundary conditions that previously would have panicked (e.g., empty work areas) and for operational timeouts/retry behavior (e.g., startup readiness deadlines).