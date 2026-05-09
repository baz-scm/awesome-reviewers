---
title: SSE and Sync Eligibility
description: 'When implementing networking/event-streaming and bidirectional sync,
  make event delivery correctness explicit: who owns the subscription, who owns cursor
  advancement, and whether an event should be echoed back.'
repository: warpdotdev/warp
label: Networking
language: Rust
comments_count: 4
repository_stars: 56893
---

When implementing networking/event-streaming and bidirectional sync, make event delivery correctness explicit: who owns the subscription, who owns cursor advancement, and whether an event should be echoed back.

Apply these rules:
1) **Differentiate event origin** (server-originated vs user-originated) before emitting a change back over the network, to prevent feedback loops.
2) **Open SSE only for eligible consumers**: exclude passive/shared/remote-run views that don’t actually receive inbox delivery in this process.
3) **Define cursor ownership**: only the component that “owns” the inbox should advance/persist cursors; avoid dormant subscribers that advance the server cursor, which can cause later replays to return nothing.
4) **Trigger on the right event classes**: don’t filter wake/delivery down to a narrow subset (e.g., only message events) if lifecycle/peer events should wake the process.

Minimal pattern:
```rust
// 1) Origin-aware echo prevention
match event {
  BufferEvent::ContentChanged { delta, origin } => {
    if origin == EventOrigin::Server {
      // Don't push back to the server; it's already accounted for.
      return;
    }
    // Push only user-originated changes.
    send_edit_to_server(delta);
  }
}

// 2) Eligibility predicate for SSE
fn is_eligible(conversation_id: AIConversationId, ctx: &AppContext) -> bool {
  let has_consumer = driver_or_view_has_live_consumer(conversation_id, ctx);
  let is_not_passive_remote_view = !is_shared_or_remote_child_view(conversation_id, ctx);
  has_consumer && is_not_passive_remote_view
}

// 3) Cursor ownership: only the SSE owner updates cursor state
if this_process_owns_inbox(conversation_id) {
  persist_cursor_sqlite(conversation_id, max_seq);
  persist_cursor_server(conversation_id, max_seq);
}
```

This prevents the common networking failures implied by the discussions: echo loops in bidirectional sync, SSEs opened for the wrong role, missed wakeups from overly narrow filters, and cursor collision that causes replay gaps after dormancy.