---
title: Choose appropriate async primitives
description: 'Select async/concurrency primitives based on your specific usage patterns
  and requirements rather than defaulting to generic solutions. Different async contexts
  benefit from different tools:'
repository: unionlabs/union
label: Concurrency
language: Rust
comments_count: 3
repository_stars: 74800
---

Select async/concurrency primitives based on your specific usage patterns and requirements rather than defaulting to generic solutions. Different async contexts benefit from different tools:

**Cancellation patterns**: Use dedicated utilities like `CancellationToken::run_until_cancelled()` instead of manual `tokio::select!` loops when you need simple cancellation logic.

```rust
// Instead of manual select loops:
loop {
    tokio::select! {
        Ok((stream, _)) = listener.accept() => { /* handle */ }
        _ = token.cancelled() => { break; }
    }
}

// Use the dedicated utility:
token.run_until_cancelled(async {
    // your async logic here
}).await;
```

**Data flow patterns**: Prefer Streams over channels when you need concurrent message processing and better debugging capabilities. Streams allow for easier composition with `.inspect()`, `.for_each_concurrent()`, and other combinators.

```rust
// Instead of channels:
let (tx, mut rx) = mpsc::channel(chunk_size);
fetch_range(tx, slice).await?;
while let Some(message) = rx.recv().await { /* handle */ }

// Use streams:
let stream = fetch_range(slice).instrument(info_span!("fetch"));
stream.for_each_concurrent(None, |message| handle_message(message)).await;
```

**Synchronization**: Use async-aware locks (like `tokio::sync::RwLock`) only when you need to hold the lock across await points. For short, synchronous critical sections, prefer `std::sync` or `parking_lot` locks for better performance.

```rust
// Use async locks only when holding across awaits:
let guard = async_lock.lock().await;
some_async_operation().await; // Lock held across await
drop(guard);

// Use sync locks for quick operations:
{
    let guard = sync_lock.lock().unwrap();
    quick_synchronous_work();
} // Lock automatically released
```

This approach reduces complexity, improves performance, and makes code more maintainable by matching the tool to the specific concurrency requirements.