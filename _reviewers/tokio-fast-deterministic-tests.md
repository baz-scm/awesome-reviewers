---
title: Fast deterministic tests
description: 'Avoid using real sleeps or delays in tests as they significantly slow
  down the test suite and can introduce flakiness. Instead, use simulated time with
  the `start_paused` parameter for time-dependent tests:'
repository: tokio-rs/tokio
label: Testing
language: Rust
comments_count: 5
repository_stars: 28989
---

Avoid using real sleeps or delays in tests as they significantly slow down the test suite and can introduce flakiness. Instead, use simulated time with the `start_paused` parameter for time-dependent tests:

```rust
// Instead of this:
#[tokio::test]
async fn slow_test() {
    // This will actually wait 500ms, making tests slow
    tokio::time::sleep(Duration::from_millis(500)).await;
    // test logic...
}

// Do this:
#[tokio::test(start_paused = true)]
async fn fast_test() {
    // This will execute immediately with simulated time
    tokio::time::sleep(Duration::from_millis(500)).await;
    // test logic...
}
```

For tests that need to respond to events or could potentially hang (like waiting for signals), consider:

1. Using channels instead of sleeps for synchronization
2. Setting appropriate timeouts to ensure tests fail clearly rather than hanging indefinitely
3. Choosing timeout values that are large enough to prevent flakiness but still allow tests to fail fast

With hundreds of tests in the codebase, even small performance improvements per test can significantly reduce the overall test execution time.