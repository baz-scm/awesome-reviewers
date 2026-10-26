---
title: Safe Failure Handling
description: Code should handle failure paths without panicking, and it should report
  errors in a safe, bounded, actionable way—especially when retrying or waiting for
  external readiness.
repository: cline/cline#v6
label: Error Handling
language: Rust
comments_count: 2
repository_stars: 70864
---

Code should handle failure paths without panicking, and it should report errors in a safe, bounded, actionable way—especially when retrying or waiting for external readiness.

Apply this standard:
1. **No panics on expected runtime conditions** (OS/work-area values, missing endpoints, child-process races). Validate inputs early and return an error or a degraded state.
2. **Sanitize diagnostics** before storing/forwarding (never retain or replay sensitive tokens/URLs/headers).
3. **Bound memory and log aggregation** for hostile/unreliable producers (e.g., processes that emit huge or unterminated output). Use fixed caps for number of lines and max line length.
4. **Make recovery actionable**: include timeout/retry guidance in returned error messages, and attach safe context (exit status, last sanitized diagnostics) when helpful.

Example pattern (validation + safe, bounded failure context):
```rust
const MAX_LINES: usize = 32;
const MAX_LINE_LEN: usize = 1024;

fn clamp_bounds(window: (i32,i32,i32,i32), work: (i32,i32,i32,i32)) -> Result<(i32,i32,i32,i32), String> {
    let (wl, wt, wr, wb) = work;
    let work_w = wr - wl;
    let work_h = wb - wt;
    if work_w <= 0 || work_h <= 0 {
        return Err("Invalid work area (empty/inverted); cannot place window safely".into());
    }

    // Use clamping with the validated (non-empty) range.
    let (l, t, r, b) = window;
    let width = (r - l).max(1).min(work_w);
    let height = (b - t).max(1).min(work_h);
    let left = l.clamp(wl, wr - width);
    let top = t.clamp(wt, wb - height);
    Ok((left, top, left + width, top + height))
}

fn record_diagnostic(mut storage: Vec<String>, line: &str) -> Vec<String> {
    // sanitize (placeholder): reject sensitive markers/tokens here
    let sanitized = line.chars().filter(|c| !c.is_control()).take(MAX_LINE_LEN).collect::<String>();
    if sanitized.is_empty() { return storage; }
    if storage.len() == MAX_LINES { storage.remove(0); }
    storage.push(sanitized);
    storage
}
```
This approach prevents crashes, avoids sensitive-data leaks, keeps memory stable, and produces errors that clearly tell users what to do next (retry/timeout) with safe context.