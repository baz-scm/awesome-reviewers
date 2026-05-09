---
title: Graceful Error Semantics
description: 'Define and implement explicit, user- and operator-facing error semantics
  for async/protocol code: handle recoverable/expected mismatches without panicking,
  make failure outcomes observable, and ensure recovery/retry behavior is bounded
  and well-specified.'
repository: warpdotdev/warp
label: Error Handling
language: Rust
comments_count: 6
repository_stars: 56893
---

Define and implement explicit, user- and operator-facing error semantics for async/protocol code: handle recoverable/expected mismatches without panicking, make failure outcomes observable, and ensure recovery/retry behavior is bounded and well-specified.

**Apply this standard**
1. **No panics for expected mismatches**: If an input/protocol branch is “unknown/unhandled” but not a security-critical invariant, do not `panic!`/`unhandled!()`. Prefer `return`/`ignore` with `log::warn!` (including the offending parameters) and continue.
2. **Async workflows must specify failure outcome**: For operations like “save”, “open”, “edit apply”, and “send”, always decide one of:
   - **Accept + respond success**
   - **Reject with a client-visible outcome** (and/or a telemetry event)
   - **Discard but explicitly report** (so the UI/workflow can reconcile)
   - **Reconcile by pushing server state** (if clients can be stale)
   - **Retry with bounded backoff** (when transient)
3. **Prevent retry/restart storms**: Any loop that can restart on clean-but-empty/closure states must include an outer backoff or a bounded retry counter.
4. **Add error context to logs/telemetry**: When possible, include the error string (or an error code/category) so failures are diagnosable without reproducing.

**Concrete examples**
- Avoid panic on protocol mismatch:
```rust
('n', Some(b'?')) => {
    match next_param_or(0) {
        996 => handler.report_color_scheme(writer),
        other => {
            log::warn!("Unhandled CSI ? Ps n query: {other}");
            // graceful no-op
        }
    }
}
```
- For edit rejection, never leave clients in an undefined state:
  - Either return a “stale edit rejected” result the UI can act on, **or** push the server’s current content/state to connected clients.
- For restart loops:
```rust
// On Ok(None) / Err, wait a little before re-opening the listener.
self.restart_backoff = self.restart_backoff.next();
warpui::async::sleep(self.restart_backoff).await;
self.start_dormant_claude_wake_listener(conversation_id, ctx);
```

**Checklist**: For any change touching error handling, confirm you can answer (a) what happens on failure, (b) whether it retries/reconciles, (c) how the user/client learns about it, and (d) where the error reason is captured (log/telemetry).