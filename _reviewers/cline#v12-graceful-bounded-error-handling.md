---
title: Graceful bounded error handling
description: Implement error handling that (1) avoids panics on expected edge cases,
  (2) bounds and sanitizes diagnostics from failing/hostile subprocess output, and
  (3) treats external-process lifecycle calls as non-authoritative about liveness—always
  re-check state when deciding whether to retry/respawn.
repository: cline/cline#v12
label: Error Handling
language: Rust
comments_count: 2
repository_stars: 70872
---

Implement error handling that (1) avoids panics on expected edge cases, (2) bounds and sanitizes diagnostics from failing/hostile subprocess output, and (3) treats external-process lifecycle calls as non-authoritative about liveness—always re-check state when deciding whether to retry/respawn.

Apply as follows:
- Prefer `Result` over `panic!/unwrap` in setup/OS integration paths. Validate inputs and, on failure, log and continue with degraded behavior.
- When capturing failure diagnostics (startup logs, stderr/stdout), enforce bounds (max lines/bytes) and sanitize sensitive content before storing/forwarding.
- For retry logic around child processes, do not assume `child.kill()`/`child.wait()` success means the process was alive. Design retries to be idempotent by re-checking with `try_wait()` and using tracked child identity (e.g., PID) before overwriting shared state.

Example (validation + graceful degradation + bounded sanitized logging):
```rust
fn clamp_window_bounds(window: WindowBounds, work_area: WindowBounds) -> Result<WindowBounds, String> {
    let work_width = work_area.right - work_area.left;
    let work_height = work_area.bottom - work_area.top;
    if work_width <= 0 || work_height <= 0 {
        return Err("invalid work area".to_string());
    }
    let width = (window.right - window.left).clamp(1, work_width);
    let height = (window.bottom - window.top).clamp(1, work_height);
    let left = window.left.clamp(work_area.left, work_area.right - width);
    let top = window.top.clamp(work_area.top, work_area.bottom - height);
    Ok(WindowBounds { left, top, right: left + width, bottom: top + height })
}

fn record_diagnostic_safely(store: &mut VecDeque<String>, line: &str, max_lines: usize) {
    let sanitized = line
        .chars()
        .filter(|c| !c.is_control())
        .take(1024)
        .collect::<String>();

    if sanitized.is_empty() { return; }
    if store.len() == max_lines { store.pop_front(); }
    store.push_back(sanitized);
}

fn should_respawn_after_kill(child: &mut std::process::Child) -> bool {
    // `kill()`/`wait()` success is not authoritative about liveness.
    // Re-check via try_wait and only then mutate shared state.
    matches!(child.try_wait(), Ok(None))
}
```