---
title: Failure-aware error handling
description: Adopt failure-mode-aware error handling that (a) chooses and documents
  a safe fallback when behavior is ambiguous, (b) degrades gracefully instead of panicking,
  and (c) makes diagnostics bounded/sanitized while keeping recovery logic race- and
  platform-semantic correct.
repository: ClInE/cLiNe
label: Error Handling
language: Rust
comments_count: 3
repository_stars: 70838
---

Adopt failure-mode-aware error handling that (a) chooses and documents a safe fallback when behavior is ambiguous, (b) degrades gracefully instead of panicking, and (c) makes diagnostics bounded/sanitized while keeping recovery logic race- and platform-semantic correct.

Practical checklist:
- Bias timeouts toward the least harmful steady state and document the reasoning for ambiguous cases.
- Replace “panic-worthy” environment/runtime assumptions with validated checks that return an error and continue with a safe fallback.
- For startup/retry loops: bound waiting time, add backoff to avoid crash loops, and ensure late/out-of-order events can’t corrupt newer state.
- Diagnostics: keep memory bounded and avoid leaking sensitive data (redact known markers; cap line sizes).
- Platform/runtime semantics: don’t treat expected lifecycle quirks (e.g., kill/wait after reap) as fatal; encode the intended interpretation.

Example pattern (bounded, sanitized diagnostics + safe fallback):
```rust
const MAX_DIAG_LINES: usize = 32;
const MAX_DIAG_LINE: usize = 1024;

fn sanitize(line: &str) -> String {
    // redact sensitive markers here
    line.chars().filter(|c| !c.is_control()).take(MAX_DIAG_LINE).collect()
}

fn record_diagnostic(diags: &mut Vec<String>, line: &str) {
    let line = sanitize(line.trim());
    if line.is_empty() { return; }
    if diags.len() == MAX_DIAG_LINES { diags.remove(0); }
    diags.push(line);
}

fn safe_fit_or_fallback(valid: bool) -> Result<(), String> {
    if !valid {
        // log + continue with a safe UI fallback instead of panicking
        return Err("window fitting failed; continuing without fitting".into());
    }
    Ok(())
}
```