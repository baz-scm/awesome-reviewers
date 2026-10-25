---
title: Graceful, bounded error handling
description: For failures and malformed inputs, implement error handling that (1)
  degrades gracefully instead of panicking, (2) preserves correctness across partial/streamed
  boundaries, and (3) reports errors safely with strict bounds.
repository: CLINE/cline
label: Error Handling
language: Rust
comments_count: 3
repository_stars: 70839
---

For failures and malformed inputs, implement error handling that (1) degrades gracefully instead of panicking, (2) preserves correctness across partial/streamed boundaries, and (3) reports errors safely with strict bounds.

Guidelines
- Avoid panics on expected edge cases
  - Validate inputs (dimensions/ranges/paths/empty workspaces). If invalid, return a controlled error and keep the app functional (log + fallback UI/service behavior).
- Handle partial/invalid streamed data deterministically
  - If bytes/frames may arrive split, don’t emit replacement/corrupted output. Preserve the incomplete suffix and re-process when more data arrives.
  - Add regression tests for tricky boundaries (e.g., invalid bytes followed by a valid completion byte).
- Make diagnostics safe and bounded
  - Never forward sensitive logs across trust boundaries; sanitize or omit records before sending to UI.
  - Bound diagnostic buffers (max lines, max line length). Truncate unterminated/oversized records and continue draining pipes so logging failures don’t stall the system.

Example pattern: stateful UTF-8 boundary handling
```rust
fn split_utf8(bytes: Vec<u8>) -> (String, Vec<u8>) {
    match std::str::from_utf8(&bytes) {
        Ok(text) => (text.to_string(), Vec::new()),
        Err(err) => {
            // Carry over only the genuinely incomplete suffix; never drop/garble valid prefix.
            let valid = err.valid_up_to();
            let carry_len = bytes.len() - valid;
            if err.error_len().is_none() && carry_len < 4 {
                (String::from_utf8_lossy(&bytes[..valid]).into_owned(), bytes[valid..].to_vec())
            } else {
                (String::from_utf8_lossy(&bytes).into_owned(), Vec::new())
            }
        }
    }
}
```

Apply this standard whenever you:
- parse streamed/byte-oriented data,
- accept external/environment inputs (window/work-area, paths, cwd, env vars), or
- propagate startup/health/error information across components.
