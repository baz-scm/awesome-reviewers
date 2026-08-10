---
title: Concurrency bookkeeping and cancel
description: When concurrency involves async tasks, cross-thread messaging, or callbacks
  from other components, prefer *explicit bookkeeping* and *bounded, non-blocking
  communication* so correctness doesn’t rely on timing.
repository: ogulcancelik/herdr
label: Concurrency
language: Rust
comments_count: 6
repository_stars: 26924
---

When concurrency involves async tasks, cross-thread messaging, or callbacks from other components, prefer *explicit bookkeeping* and *bounded, non-blocking communication* so correctness doesn’t rely on timing.

Apply these rules:
1) **Make callbacks stale-proof**: tag work with a `generation`/`request_id` and ignore results from prior generations.
2) **Prevent duplicate side-effects**: use a single-claim latch (e.g., `Arc<AtomicBool>`) so only one caller performs teardown/restore.
3) **Track outstanding operations, don’t assume ordering**: maintain a shared pending counter/state so framing/processing logic can distinguish “waiting for completion” vs “idle”.
4) **Cancellation must be real**: cancel/abort should terminate the entire execution context (e.g., subprocess process group/job) and add a regression test for descendant survival.
5) **Avoid blocking critical threads on backpressure**: use bounded channels with `try_send`/best-effort semantics or timeouts; never let PTY/UI reader loops wait on slow consumers.

Example pattern (stale-proof + single-restore + pending counter):

```rust
use std::sync::{Arc, atomic::{AtomicBool, Ordering}};

struct Guard {
    restored: Arc<AtomicBool>,
}
impl Drop for Guard {
    fn drop(&mut self) {
        if !self.restored.swap(true, Ordering::AcqRel) {
            restore_terminal_state(); // runs once
        }
    }
}

// Ignore stale async results.
fn handle_finished(generation: u64, current: u64, value: Option<String>) {
    if generation != current { return; }
    // safe to apply
}

// Outstanding-query tracking for interleaved replies.
struct Pending { count: u32 }
impl Pending {
    fn arm(&mut self) { self.count = self.count.saturating_add(1); }
    fn drain_before_frame(&mut self) -> u32 { std::mem::take(&mut self.count) }
}
```

This reduces races/TOCTOU reliance, prevents mis-framing and double-restore bugs, and keeps the system responsive under load.