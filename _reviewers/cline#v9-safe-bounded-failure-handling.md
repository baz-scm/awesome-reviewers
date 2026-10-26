---
title: Safe bounded failure handling
description: When code can fail (startup, IPC/process lifecycle, platform fitting,
  IO), handle errors in a way that is (1) safe (no sensitive leakage), (2) bounded
  (time/memory), and (3) recoverable without panicking.
repository: cline/cline#v9
label: Error Handling
language: Rust
comments_count: 2
repository_stars: 70868
---

When code can fail (startup, IPC/process lifecycle, platform fitting, IO), handle errors in a way that is (1) safe (no sensitive leakage), (2) bounded (time/memory), and (3) recoverable without panicking.

Apply these rules:
1) Sanitize and bound diagnostic data
- If failures involve logs/outputs, store only safe, bounded diagnostics.
- Redact or omit content that may contain secrets, and cap per-line length and stored history.

2) Use timeouts + backoff for recovery
- For “wait for readiness” flows, use an explicit deadline and poll interval.
- If you retry by respawning/kicking off recovery, pace it with a backoff to avoid crash loops.

3) Avoid panics in error-prone boundaries
- Validate inputs early (e.g., empty/inverted OS-provided work areas).
- Return a Result with an error that calling code can log/handle, instead of letting arithmetic guards lead to panics.

4) Make retry/stop logic robust to lifecycle races
- Assume the process may already have exited; ensure kill/wait/try_wait outcomes don’t break the retry state machine.

Example pattern (bounded, sanitized diagnostics + time-bounded readiness loop):
```rust
const MAX_LINES: usize = 32;
const MAX_LINE_BYTES: usize = 1024;
const WAIT_TOTAL: std::time::Duration = std::time::Duration::from_secs(30);
const WAIT_POLL: std::time::Duration = std::time::Duration::from_millis(100);

fn sanitize(line: &str) -> Option<String> {
    // Omit/redact sensitive markers here
    let trimmed = line.trim();
    if trimmed.is_empty() { return None; }
    Some(trimmed.chars().filter(|c| !c.is_control()).take(MAX_LINE_BYTES).collect())
}

fn wait_for_ready(get_endpoint: impl Fn() -> Option<String>) -> Result<String, String> {
    let deadline = std::time::Instant::now() + WAIT_TOTAL;
    while std::time::Instant::now() < deadline {
        if let Some(ep) = get_endpoint() { return Ok(ep); }
        std::thread::sleep(WAIT_POLL);
    }
    Err("Backend did not publish its endpoint in time (retry startup)".to_string())
}
```

Result: failures become observable and actionable (clear status/errors), resources stay bounded (no runaway memory/IO), secrets aren’t exposed, and recovery is dependable instead of crashing the app.