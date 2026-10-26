---
title: Safe Error Recovery
description: 'When code can fail (platform inputs, subprocess startup, IPC), handle
  failures as *controlled, bounded, non-leaky* paths: avoid panics, convert failures
  into actionable error states/messages, and (when recovery is plausible) retry with
  backoff/timeouts.'
repository: cline/cline#v18
label: Error Handling
language: Rust
comments_count: 2
repository_stars: 70884
---

When code can fail (platform inputs, subprocess startup, IPC), handle failures as *controlled, bounded, non-leaky* paths: avoid panics, convert failures into actionable error states/messages, and (when recovery is plausible) retry with backoff/timeouts.

**Standard checklist**
- **Don’t panic on bad inputs:** validate external/platform-derived values; on invalid state return an error, log it, and degrade gracefully (keep the app responsive).
- **Bound diagnostic/resource usage:** cap retained log/diagnostic lines and line lengths so a misbehaving process can’t exhaust memory (including unterminated outputs).
- **Sanitize anything surfaced to UI:** if diagnostics may contain secrets (URLs, tokens, headers), redact/omit matching markers and avoid replaying raw logs.
- **Make failures user-actionable:** set clear error strings (e.g., “endpoint not published… retry startup”) and record enough context to debug without leaking sensitive data.
- **Recover when possible:** use timeouts and respawn/retry logic with **backoff**; ensure shutdown/cleanup paths don’t orphan processes or wipe successor state.

**Pattern example (validation + bounded, sanitized diagnostics)**
```rust
const MAX_LINES: usize = 32;
const MAX_LINE_LEN: usize = 1024;

fn validate_work_area(work_area: (i32, i32, i32, i32)) -> Result<(), String> {
    let (_l, _t, r, b) = work_area;
    if r <= 0 || b <= 0 {
        return Err("invalid work area from OS".to_string());
    }
    Ok(())
}

fn sanitize_line(line: &str) -> String {
    // redact known sensitive markers
    let lower = line.to_ascii_lowercase();
    if lower.contains("token=") || lower.contains("oauth") {
        return "[Sensitive output omitted]".to_string();
    }
    line.chars().filter(|c| !c.is_control()).take(MAX_LINE_LEN).collect()
}

fn record_diagnostic(diags: &mut Vec<String>, line: &str) {
    let line = sanitize_line(line.trim());
    if line.is_empty() { return; }
    if diags.len() == MAX_LINES { diags.remove(0); }
    diags.push(line);
}
```