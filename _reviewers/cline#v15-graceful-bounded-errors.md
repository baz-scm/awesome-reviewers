---
title: Graceful, bounded errors
description: 'When handling failures, avoid crash paths and ensure recovery is safe
  and observable:


  - Validate inputs/assumptions before using range-dependent operations; if invalid,
  return an error (or degrade safely) rather than panicking.'
repository: cline/cline#v15
label: Error Handling
language: Rust
comments_count: 2
repository_stars: 70877
---

When handling failures, avoid crash paths and ensure recovery is safe and observable:

- Validate inputs/assumptions before using range-dependent operations; if invalid, return an error (or degrade safely) rather than panicking.
- Bound any failure-related resource usage (e.g., diagnostic buffers/line lengths) so a misbehaving component cannot exhaust memory.
- Sanitize any diagnostics or error text that might include secrets (tokens, URLs, headers) before persisting or forwarding.
- On readiness timeouts or recovery failures, return an actionable message that includes *bounded, sanitized* context and triggers retry/recovery where appropriate.
- Add regression tests for the edge cases that previously caused panics or uncontrolled growth.

Example (pattern):
```rust
const MAX_LINES: usize = 32;
const MAX_LINE_LEN: usize = 1024;

fn sanitize_diagnostic(line: &str) -> String {
    // Replace/omit secret-bearing markers; keep output bounded.
    // (Implementation should be tailored to your marker set.)
    line.chars().filter(|c| !c.is_control()).take(MAX_LINE_LEN).collect()
}

fn record_diagnostic(diags: &mut std::collections::VecDeque<String>, line: &str) {
    let line = sanitize_diagnostic(line.trim());
    if line.is_empty() { return; }
    if diags.len() == MAX_LINES { diags.pop_front(); }
    diags.push_back(line);
}

// Prefer graceful error over panic for invalid inputs.
fn clamp_value_or_error(x: i32, min: i32, max: i32) -> Result<i32, String> {
    if min > max { return Err("invalid range".to_string()); }
    Ok(x.clamp(min, max))
}
```
Use this standard especially around: background process readiness, IPC/endpoint discovery, and UI/window geometry computations where invalid inputs or excessive logs are plausible.