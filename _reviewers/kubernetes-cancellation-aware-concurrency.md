---
title: Cancellation Aware Concurrency
description: 'When adding or modifying concurrent code, treat context/cancellation,
  goroutine lifecycle, and state ownership as first-class requirements.


  Practical standards:'
repository: kUbernetes/kUbernetes
label: Concurrency
language: Go
comments_count: 11
repository_stars: 128688
---

When adding or modifying concurrent code, treat context/cancellation, goroutine lifecycle, and state ownership as first-class requirements.

Practical standards:
1) Always pass the caller’s ctx down the call chain
- If a worker can be stopped (pod workers, termination syncing, request handlers), Sync*/kill/runtime methods must accept and use the passed ctx (as parent) rather than recreating contexts.

2) Never block forever on goroutine completion
- Avoid patterns like `wg.Wait()` or “wait for completion” that can’t be released when ctx is cancelled.
- Prefer cancellation-aware `select` loops and/or separate completion channels that can be selected against `ctx.Done()`.

3) Don’t share mutable variables between goroutines
- If a goroutine needs to report `err`/results, send them over a `chan` (or use a thread-safe primitive). Avoid capturing a local variable and writing to it concurrently.

4) Make teardown cancellation effective
- If you wrap clocks/transports/watchers, use the fixture/test ctx (or a derived cancelable ctx), not `context.Background()`, so injected delays/faults terminate on cleanup.

5) Ensure async goroutines don’t outlive tests/owner scopes
- In tests, wait for background goroutines to exit (or stop them via cancel/close and then `<-done`). Avoid “log after test complete” races.

6) State handovers must have clear ownership and ordering
- During retries/handovers (leader election recovery, DRA health stream generation, termination ordering), ensure the new owner synchronously takes control so old goroutines can’t overwrite/clear state after ownership transfer.

7) Test isolation under concurrency
- If you mutate global state (e.g., package-level clocks), document and enforce “no parallel tests” in the same process.

Illustrative patterns:

A) Cancel-aware goroutine completion without shared err
```go
errCh := make(chan error, 1)
go func() {
    // compute / call that may block
    errCh <- runtimeService.StopContainer(ctx, id, grace)
}()
select {
case <-ctx.Done():
    // caller cancelled; return quickly
    return ctx.Err()
case err := <-errCh:
    return err
}
```

B) Goroutine leak prevention in tests
```go
done := make(chan struct{})
go func() {
    defer close(done)
    _ = obj.Run(ctx, sourcesReady)
}()
// ... trigger stop
cancel()          // or close(stopCh)
<-done            // wait until Run actually exits
```

C) Don’t hide non-cancellable waits
- If injected behavior (delays/faults/watch loops) can block, ensure it can observe the same cancel signal as the test/fixture teardown.