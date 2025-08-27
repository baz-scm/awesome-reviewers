---
title: avoid timing dependencies
description: Eliminate timing dependencies in tests by using proper retry mechanisms
  and assertions instead of sleep statements. Sleep-based waits make tests flaky and
  unreliable, while retry mechanisms with conditions provide more robust test execution.
repository: istio/istio
label: Testing
language: Go
comments_count: 3
repository_stars: 37192
---

Eliminate timing dependencies in tests by using proper retry mechanisms and assertions instead of sleep statements. Sleep-based waits make tests flaky and unreliable, while retry mechanisms with conditions provide more robust test execution.

Replace `time.Sleep()` calls with `assert.EventuallyEqual()` or appropriate retry functions that wait for specific conditions to be met. Choose `retry.Converge()` over `retry.MaxAttempts()` when you need consistent state verification, as it waits for multiple consecutive successful checks rather than potentially giving up early during system startup.

Example of problematic code:
```go
time.Sleep(2 * time.Second) // wait for the namespace to be created
```

Preferred approach:
```go
assert.EventuallyEqual(t, func() int {
    se := rig.se.Get("pre-existing", "default")
    return len(autoallocate.GetAddressesFromServiceEntry(se))
}, 2, retry.Converge(10), retry.Delay(time.Millisecond*5))
```

This approach makes tests more reliable by waiting for actual conditions rather than arbitrary time periods, reducing flakiness and improving test execution speed.