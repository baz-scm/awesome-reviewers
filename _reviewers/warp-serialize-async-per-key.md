---
title: Serialize async per-key
description: Ensure async/stateful flows are race-free by avoiding overlapping work
  for the same logical key and by handling events that arrive before the relevant
  state is ready.
repository: warpdotdev/warp
label: Concurrency
language: Rust
comments_count: 5
repository_stars: 56893
---

Ensure async/stateful flows are race-free by avoiding overlapping work for the same logical key and by handling events that arrive before the relevant state is ready.

Practical rules:
- If multiple updates for the same key (e.g., `path`, `session_id`, `conversation_id`) can be triggered concurrently, allow only one in-flight async task per key. Queue subsequent updates and apply them sequentially after the current task completes.
- If an external event can arrive before initialization/handshake finishes, do not drop it due to temporarily-missing state. Buffer the specific safe event(s) and replay/emit them after the session transitions to the ready state.
- Don’t rely on side-effects that normally happen via subscriptions/entry hooks when control flow can short-circuit. Apply the required state change immediately at the callsite.
- Avoid blocking filesystem/UI work: if filesystem checks could require syscalls, perform them off the main thread and/or in bounded async work.

Example (per-key queue to prevent stale overwrites):
```rust
// pseudo-pattern
if let Some(queued) = pending_updates.get_mut(&key) {
    queued.push(update);
    return;
}

pending_updates.insert(key.clone(), Vec::new());
let rules = current_rules.clone();
spawn(async move {
    process_update(update, rules, key.clone()).await
}, move |me, result, ctx| {
    me.apply(result);
    me.drain_pending_updates(&key, ctx); // sequentially process queued updates
});
```