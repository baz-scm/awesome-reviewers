---
title: Minimize cross-device transfers
description: Data transfers between different compute devices (CPU/host to GPU/accelerator
  and back) can significantly impact performance in heterogeneous computing environments.
  Each transfer introduces latency and can block computation pipelines. Pay special
  attention to round-trip patterns where data moves from device A to B and back to
  A, as these create...
repository: tensorflow/swift
label: Performance Optimization
language: Markdown
comments_count: 2
repository_stars: 6136
---

Data transfers between different compute devices (CPU/host to GPU/accelerator and back) can significantly impact performance in heterogeneous computing environments. Each transfer introduces latency and can block computation pipelines. Pay special attention to round-trip patterns where data moves from device A to B and back to A, as these create synchronization points that stall execution.

For optimal performance:
1. Minimize data movement between host and accelerator during performance-critical sections
2. Batch transfers when possible rather than transferring small pieces repeatedly
3. Be especially wary of transfers inside loops that can repeatedly block computation

Watch for problematic patterns like this:
```
for step in 0...1000 {
  let gradients = ... // on accelerator
  weights += gradients // on accelerator
  if cpuOnlyFunc(weights) == 0 { // forces data transfer to CPU and back
    weights += 1 // continues on accelerator after blocking
  }
}
```

When designing APIs that operate across device boundaries, consider providing asynchronous alternatives that allow computation to continue without blocking while transfers occur in the background.
