---
title: Minimize blocking operations
description: When writing concurrent code, minimize blocking operations to maintain
  responsiveness and prevent performance bottlenecks. This applies especially to async
  contexts and lock usage.
repository: openai/codex
label: Concurrency
language: Rust
comments_count: 4
repository_stars: 31275
---

When writing concurrent code, minimize blocking operations to maintain responsiveness and prevent performance bottlenecks. This applies especially to async contexts and lock usage.

For asynchronous operations:
- Prefer `tokio::spawn` over thread creation for concurrent tasks, as it's more lightweight
- Run independent operations in parallel when possible
- Keep critical startup paths non-blocking by moving potentially slow operations to background tasks

For lock handling:
- Keep lock durations as short as possible by using tight scoping
- Release locks immediately after use to prevent contention
- Use single-statement operations when possible to minimize lock holding time

Example - Before:
```rust
{
    let mut running_requests_id_to_codex_uuid = running_requests_id_to_codex_uuid.lock().await;
    running_requests_id_to_codex_uuid.insert(request_id.clone(), session_id);
}
```

After:
```rust
running_requests_id_to_codex_uuid.lock().await.insert(request_id.clone(), session_id);
```

For mutex usage:
```rust
// Bad: Lock held longer than necessary
let mut flag = self.pending_redraw.lock().unwrap();
if *flag {
    return;
}
*flag = true;
// Lock still held here when it's no longer needed

// Good: Lock released as soon as possible
{
    let mut flag = self.pending_redraw.lock().unwrap();
    if *flag {
        return;
    }
    *flag = true;
} // Lock released here
// Continue with operations that don't need the lock
```