---
title: Fail safely and recover
description: When handling startup/runtime failures, ensure code (1) never panics
  on expected edge cases, (2) captures only safe, bounded diagnostics, and (3) recovers
  deterministically with explicit timeouts/backoff that tolerate real OS/process semantics.
repository: Cline/Cline
label: Error Handling
language: Rust
comments_count: 2
repository_stars: 70840
---

When handling startup/runtime failures, ensure code (1) never panics on expected edge cases, (2) captures only safe, bounded diagnostics, and (3) recovers deterministically with explicit timeouts/backoff that tolerate real OS/process semantics.

Apply this standard:
- Validate inputs/OS state before computing ranges or bounds; if invalid, return an error and degrade gracefully (log and continue showing UI, rather than crashing).
- For failure diagnostics:
  - Sanitize before storing/forwarding (avoid retaining sensitive tokens/URLs/headers).
  - Bound memory and output size (cap lines/chars and handle unterminated/oversized records).
- For recovery:
  - Use explicit timeouts for “ready” conditions.
  - Use backoff to avoid respawn loops.
  - Treat lifecycle operations on already-exited processes as success where the platform/std guarantees it.

Example pattern (Rust):
```rust
fn sanitize_line(line: &str) -> String {
    let lower = line.to_ascii_lowercase();
    if lower.contains("access_token") {
        return "[Sensitive startup diagnostic omitted]".to_string();
    }
    line.chars().filter(|c| !c.is_control()).take(1024).collect()
}

fn try_set_bounds(window: Bounds, work_area: Bounds) -> Result<Bounds, String> {
    // Validate instead of panicking on edge cases.
    if work_area.width() <= 0 || work_area.height() <= 0 {
        return Err("invalid work area".to_string());
    }
    Ok(clamp_to_work_area(window, work_area))
}

// Recovery with timeout + backoff.
fn wait_for_ready_with_recovery(/* state, spawn */) -> Result<String, String> {
    // while not ready:
    // - if timed out: return a safe error summary using sanitized, bounded diagnostics
    // - if child exited: respawn with backoff
    // - on stop/retry: tolerate kill-after-exit semantics
    unimplemented!()
}
```

This prevents crash-on-edge-case regressions, avoids leaking sensitive data in logs, and makes retries/respanws predictable for users.