---
title: Deterministic Test Hygiene
description: 'Adopt a consistent testing standard that prevents flaky behavior, leaked
  goroutines, and false positives.


  **1) Always register cleanup for started resources**'
repository: maximhq/bifrost
label: Testing
language: Go
comments_count: 8
repository_stars: 6862
---

Adopt a consistent testing standard that prevents flaky behavior, leaked goroutines, and false positives.

**1) Always register cleanup for started resources**
- Prefer `t.Cleanup(...)` / `tb.Cleanup(...)` over scattered `defer`s.
- Use it for: clients, servers, accumulators/tickers, streaming helpers, and `Init(...)` results.

```go
bf, err := Init(ctx, cfg)
require.NoError(t, err)
t.Cleanup(func() { bf.Shutdown() })
```

**2) Make concurrency/time-sensitive tests deterministic**
- Avoid fixed sleeps like `time.Sleep(3 * time.Millisecond)` for synchronization.
- Use a bounded poll/wait with a deadline.

```go
deadline := time.Now().Add(2 * time.Second)
for time.Now().Before(deadline) {
  if body.closeCount.Load() > 0 { break }
  time.Sleep(2 * time.Millisecond)
}
stop(); cleanup()
```

**3) Ensure assertions are non-vacuous and validate invariants**
- Don’t rely on branches that may skip the assertion.
- Assert the exact behavior that should occur (e.g., “role dropped” or “snapshot deep-copied”).

```go
attachBilledUsageFromContext(ctx, bifrostErr)
// Mutate original after attach; snapshot must not change.
usage.PromptTokens = 999
require.Equal(t, 10, bifrostErr.ExtraFields.BilledUsage.PromptTokens)
```

**4) Keep mocks faithful to production side effects/commit semantics**
- If production “updates only on success,” mocks must not mutate global/shared state until validation passes.
- Avoid pointer-aliasing bugs where rollback logic doesn’t fully revert state.

```go
candidate := budgets[i]          // copy
candidate.IsCalendarAligned = calendarAligned
if err := candidate.SetOverrideAt(...); err != nil { return nil, err }
budgets[i] = candidate          // commit only on success
```

**5) Fail fast during test setup**
- When setup steps can fail (e.g., sending initial chunks), check return values immediately and `t.Fatalf(...)` with a setup-specific message.
- This prevents cascaded failures that obscure the root cause.

```go
if ok := a.GateSend(traceID, chunk0, false, false, ch, ctx); !ok {
  t.Fatalf("setup chunk 0: GateSend returned false")
}
```