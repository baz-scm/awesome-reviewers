---
title: Avoid busy waiting
description: When implementing concurrent code that waits for conditions to be met,
  avoid busy-wait loops that continuously consume CPU resources. Busy-waiting wastes
  processing power, reduces overall system performance, and can increase power consumption.
repository: dotnet/runtime
label: Concurrency
language: C#
comments_count: 5
repository_stars: 16578
---

When implementing concurrent code that waits for conditions to be met, avoid busy-wait loops that continuously consume CPU resources. Busy-waiting wastes processing power, reduces overall system performance, and can increase power consumption.

Instead, use proper synchronization primitives or give up execution time:

```csharp
// Bad practice - continuously consumes CPU
bool receivedSignal = false;
while (!receivedSignal) { }

// Better option 1 - use synchronization primitives
var signal = new ManualResetEventSlim(false);
signal.Wait(timeoutMs); // Efficiently waits without consuming CPU
// In signal handler: signal.Set();

// Better option 2 - at minimum, yield execution time
while (!receivedSignal) 
{
    Thread.Sleep(1); // Or Thread.Yield()
}
```

For more complex scenarios, consider higher-level synchronization constructs like `SemaphoreSlim`, `AutoResetEvent`, or async/await patterns with `TaskCompletionSource`. These approaches not only improve performance but also make your concurrent code more maintainable and less error-prone.
