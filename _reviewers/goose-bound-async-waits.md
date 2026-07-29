---
title: Bound async waits
description: 'In async/concurrent code, always make cancellation/timeout behavior
  correct, deterministic, and safe against stale work.


  **Coding standard**

  1) **Bound the full operation**: put `tokio::time::timeout` around the *entire*
  request/handshake/startup sequence that must not hang (including setup/config/mode
  steps).'
repository: aaif-goose/goose
label: Concurrency
language: Rust
comments_count: 9
repository_stars: 51876
---

In async/concurrent code, always make cancellation/timeout behavior correct, deterministic, and safe against stale work.

**Coding standard**
1) **Bound the full operation**: put `tokio::time::timeout` around the *entire* request/handshake/startup sequence that must not hang (including setup/config/mode steps).
2) **Cancel/cleanup what you own**: if a timed-out Future is dropped, ensure any spawned process/task owned by that component is cleaned up via `kill_on_drop(true)` or cancellation-aware control messages. Also propagate cancellation tokens into nested operations.
3) **Race stream polling vs cancellation**: don’t rely on `stream.next().await` to return on cancel; use `tokio::select!` and forward `provider.cancel(...)`. Ensure cancel forwarding still happens even if the consumer drops the stream.
4) **Reject stale updates**: when superseding sessions/providers, use a generation key (e.g., `active_session_id`) set only after successful setup; drop notifications/updates whose id doesn’t match. Abort/clear old notification receiver tasks on provider recreation.
5) **Don’t lose ordered protocol messages**: use awaited `send()` (not lossy `try_send`) for ordered streams where sequence/termination matters.

**Pattern (timeout + cancellation forwarding + stale filtering)**
```rust
use tokio::{select, time};

let models = time::timeout(SUPPORTED_MODELS_TIMEOUT, async {
    let provider = create_provider().await?;
    provider.fetch_supported_models().await
}).await??;

// In an event loop handling session notifications:
let active_session_id = /* set only after successful session/new */;
while let Some(update) = rx.recv().await {
    if update.session_id != active_session_id { continue; }
    handle_update(update);
}

// In a provider reply loop:
loop {
    let next = select! {
        biased;
        _ = cancel_token.cancelled() => {
            provider.cancel(&session_id).await;
            break;
        }
        msg = stream.next() => msg,
    };
    if next.is_none() { break; }
    handle_msg(next.unwrap());
}
```

Adopting this standard prevents: (a) hung handshakes that outlive the caller, (b) orphaned child processes after timeout, (c) “cancel didn’t stop backend” bugs, (d) stale session/provider updates corrupting state, and (e) ordering/termination regressions in protocol streams.