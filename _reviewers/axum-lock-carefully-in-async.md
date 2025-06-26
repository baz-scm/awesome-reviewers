---
title: "Lock carefully in async"
description: "When using locks in async code, follow critical guidelines to avoid deadlocks. Never hold std::sync::Mutex locks across .await points as this can cause deadlocks even in single-threaded runtimes. Use tokio::sync::Mutex when the lock needs to be held across await points."
repository: "tokio-rs/axum"
label: "Concurrency"
language: "Rust"
comments_count: 4
repository_stars: 22100
---

When using locks in async code, follow these critical guidelines:

1. Never hold `std::sync::Mutex` locks across `.await` points as this can cause deadlocks even in single-threaded runtimes. Use `tokio::sync::Mutex` when the lock needs to be held across await points.

2. Consider lock granularity carefully - avoid overly fine-grained locking that could increase complexity and potential deadlocks.

Example of proper mutex usage in async context:

```rust
#[derive(Clone)]
struct AppState {
    // Coarse-grained locking - entire data structure under one lock
    data: Arc<tokio::sync::Mutex<ComplexData>>,
    
    // Fine-grained locking - only when specifically needed
    // Note: Choose granularity based on your specific use case
    counters: Arc<std::sync::Mutex<Counters>>,
}

async fn handle_request(state: AppState) {
    // OK: std::sync::Mutex for quick operations without .await
    let count = state.counters.lock().unwrap().get_count();
    
    // OK: tokio::sync::Mutex for operations involving .await
    let mut data = state.data.lock().await;
    data.update_with_async_operation().await;
} // locks are automatically released at end of scope
```

Remember: The choice between `std::sync::Mutex` and `tokio::sync::Mutex` isn't about thread safety, but about async compatibility. `std::sync::Mutex` is thread-safe but can deadlock if held across `.await` points.