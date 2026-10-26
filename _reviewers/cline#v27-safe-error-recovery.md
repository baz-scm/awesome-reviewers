---
title: Safe Error Recovery
description: 'When failures are possible (invalid/partial inputs, ambiguous timeouts,
  startup races, platform edge cases), handle errors deterministically and safely:
  choose the least harmful outcome, avoid panics, make diagnostics safe and bounded,
  and ensure async/stale events can’t overwrite current state.'
repository: cline/cline#v27
label: Error Handling
language: Rust
comments_count: 4
repository_stars: 70892
---

When failures are possible (invalid/partial inputs, ambiguous timeouts, startup races, platform edge cases), handle errors deterministically and safely: choose the least harmful outcome, avoid panics, make diagnostics safe and bounded, and ensure async/stale events can’t overwrite current state.

Practical rules:
1) For streaming/partial data, explicitly recover from invalid or incomplete segments (carry only the incomplete suffix; replace only genuinely invalid spans deterministically), rather than letting the default decoder behavior produce noisy/incorrect output.
2) For timeout/ambiguity, pick the cheaper failure mode and document the reasoning in the code. Avoid blocking critical threads while probing.
3) For retries/startup, build a “failure pipeline”:
   - Sanitize/omit potentially sensitive log/diagnostic content.
   - Bound diagnostic storage (max lines/length) to prevent memory blowups on noisy failure.
   - Use retry/respawn with backoff and clear termination conditions.
   - Guard state updates so late/old goroutines/threads can’t clobber newer state (e.g., compare child PID/instance id before writing).
4) Replace “can panic” logic with validation and error returns at boundaries; fail gracefully (log + recover or degrade) and add regression tests for empty/inverted/out-of-range edge inputs.

Example pattern (safe diagnostics + stale-event guard):
```rust
fn record_safe_diagnostic(state: &State, raw: &str) {
    let sanitized = sanitize_and_truncate(raw); // omit sensitive markers, strip control chars, cap length
    if sanitized.is_empty() { return; }
    let mut d = state.diagnostics.lock().unwrap();
    if d.lines.len() == MAX_LINES { d.lines.pop_front(); }
    d.lines.push_back(sanitized);
}

fn handle_ready_line(state: Arc<State>, instance_id: u64, line: &str) {
    if !is_ready(line) { return; }
    // Prevent stale/late events from overwriting current endpoint.
    let current = state.current_instance_id();
    if current != instance_id || state.is_shutting_down() { return; }
    state.set_endpoint(extract_endpoint(line));
}
```