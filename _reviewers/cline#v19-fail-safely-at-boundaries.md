---
title: Fail Safely at Boundaries
description: 'When code crosses boundaries (stream chunking, IPC/process sidecars,
  platform APIs), treat malformed/partial data and failure paths as normal:

  - Validate inputs and prevent panics in app-critical flows; prefer returning a recoverable
  error and a safe fallback.'
repository: cline/cline#v19
label: Error Handling
language: Rust
comments_count: 3
repository_stars: 70885
---

When code crosses boundaries (stream chunking, IPC/process sidecars, platform APIs), treat malformed/partial data and failure paths as normal:
- Validate inputs and prevent panics in app-critical flows; prefer returning a recoverable error and a safe fallback.
- For streaming/chunked data, preserve only the truly incomplete suffix; handle invalid spans explicitly so output doesn’t degrade into replacement-corruption.
- For error/diagnostic reporting across boundaries, sanitize/omit sensitive content and bound all buffers (especially for unterminated/oversized logs). Keep memory usage predictable and ensure timeouts/backoff produce an actionable failure message.

Practical checklist
- Boundary data: add tests for tricky split cases (e.g., multi-byte sequences split across reads).
- Untrusted logs/errors: filter sensitive markers, strip control chars, cap per-line length and total stored lines.
- Failure modes: use timeouts + backoff for retries/respawns; degrade (render UI / reveal window) rather than crashing.
- Platform values: check for zero-size/inverted ranges; return errors instead of relying on “should never happen” assumptions.

Example (streaming boundary handling)
```rust
fn split_utf8(bytes: Vec<u8>) -> (String, Vec<u8>) {
    match std::str::from_utf8(&bytes) {
        Ok(text) => (text.to_string(), Vec::new()),
        Err(error) => {
            // valid_up_to => prefix is valid UTF-8; remainder may be incomplete.
            let valid = error.valid_up_to();
            let carry_len = bytes.len() - valid;
            if error.error_len().is_none() && carry_len < 4 {
                // Only carry over an incomplete suffix.
                let text = String::from_utf8_lossy(&bytes[..valid]).into_owned();
                (text, bytes[valid..].to_vec())
            } else {
                // For invalid spans, don’t corrupt output—fall back safely.
                (String::from_utf8_lossy(&bytes).into_owned(), Vec::new())
            }
        }
    }
}
```
