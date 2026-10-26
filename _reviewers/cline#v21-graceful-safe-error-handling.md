---
title: Graceful, Safe Error Handling
description: Adopt an error-handling standard that (1) prevents crashes on edge cases
  and (2) turns external/volatile failure signals (like child-process logs) into bounded,
  sanitized, user-safe diagnostics with clear recovery.
repository: cline/cline#v21
label: Error Handling
language: Rust
comments_count: 2
repository_stars: 70886
---

Adopt an error-handling standard that (1) prevents crashes on edge cases and (2) turns external/volatile failure signals (like child-process logs) into bounded, sanitized, user-safe diagnostics with clear recovery.

Practical rules:
- Avoid panics on expected edge cases: validate inputs before calling operations that can panic (or use fallible variants). If preconditions don’t hold, return/propagate a controlled error so the app can degrade or continue.
- When consuming logs/errors from external processes:
  - Sanitize/omit sensitive content before storing or replaying it.
  - Bound memory and parsing (e.g., limit line length and stored diagnostic lines) to prevent runaway behavior.
  - Keep draining stdout/stderr even if the sink/forwarder fails, so the child can’t block on full pipes.
- Use timeouts + paced retry/respawn for startup readiness failures, and surface a clear failure message when recovery doesn’t succeed.

Code pattern (fallible validation instead of panic):
```rust
// Example: avoid panics on degenerate ranges by validating and returning an error.
fn safe_clamp_range(value: i32, min: i32, max: i32) -> Result<i32, String> {
    if min >= max {
        return Err("invalid range".to_string());
    }
    Ok(value.clamp(min, max))
}
```

Code pattern (bounded + sanitized diagnostic storage):
```rust
fn record_diagnostic(store: &mut std::collections::VecDeque<String>, line: &str) {
    const MAX_LINES: usize = 32;
    const MAX_LINE_LEN: usize = 1024;

    // sanitize (example: drop control chars / omit sensitive markers)
    let sanitized: String = line.chars()
        .filter(|c| !c.is_control())
        .take(MAX_LINE_LEN)
        .collect();

    if sanitized.is_empty() { return; }
    if store.len() == MAX_LINES { store.pop_front(); }
    store.push_back(sanitized);
}
```

Outcome: failures become recoverable and diagnosable without leaking secrets or risking unbounded resource usage, and the application avoids crashing due to predictable edge cases.