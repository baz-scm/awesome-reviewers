---
title: Graceful, sanitized error paths
description: 'When handling failures (invalid inputs, process startup, endpoint readiness,
  etc.), do not panic or expose sensitive details. Instead:


  - Fail gracefully: convert edge cases into recoverable errors/status updates (log
  + keep the app usable where possible).'
repository: cline/cline#v7
label: Error Handling
language: Rust
comments_count: 2
repository_stars: 70865
---

When handling failures (invalid inputs, process startup, endpoint readiness, etc.), do not panic or expose sensitive details. Instead:

- Fail gracefully: convert edge cases into recoverable errors/status updates (log + keep the app usable where possible).
- Bound diagnostics: cap stored and forwarded diagnostic volume/line length to prevent unbounded memory growth.
- Sanitize sensitive output: omit or redact secrets (tokens, auth URLs/headers, etc.) before persisting or forwarding logs to other layers.
- Provide actionable messages: user-facing/status errors should explain what failed and what to do next (e.g., “Retry startup.”).
- Recover deterministically: if appropriate, retry with explicit timeouts and backoff; ensure failure states are recorded and that retries don’t spawn duplicates.

Example pattern (bounded + sanitized diagnostics + actionable failure):

```rust
const MAX_LINES: usize = 32;
const MAX_LINE_LEN: usize = 1024;

fn sanitize(line: &str) -> String {
    // Example: redact known sensitive markers
    let lower = line.to_ascii_lowercase();
    if lower.contains("token") || lower.contains("oauth") {
        "[Sensitive output omitted]".to_string()
    } else {
        line.chars().take(MAX_LINE_LEN).collect()
    }
}

fn record_startup_failure(diags: &mut Vec<String>, line: &str) {
    let s = sanitize(line.trim());
    if s.is_empty() { return; }
    if diags.len() == MAX_LINES { diags.remove(0); }
    diags.push(s);
}

// On timeout:
// return Err("Desktop backend did not publish its endpoint. Retry startup.".to_string())
```

This applies both to environment/input validation (avoid panics on unexpected geometry/config) and to sidecar/process readiness (bounded, sanitized diagnostics + controlled retry/recovery).