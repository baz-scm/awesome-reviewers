---
title: Graceful Error Propagation
description: When writing library code, never hard-terminate or silently ignore failures.
  Always (1) validate inputs/shape compatibility correctly (including pack/elempack
  and dynamic dims), (2) signal errors with consistent return codes, and (3) propagate
  error statuses from lower-level operations to the caller.
repository: Tencent/ncnn
label: Error Handling
language: C++
comments_count: 6
repository_stars: 23205
---

When writing library code, never hard-terminate or silently ignore failures. Always (1) validate inputs/shape compatibility correctly (including pack/elempack and dynamic dims), (2) signal errors with consistent return codes, and (3) propagate error statuses from lower-level operations to the caller.

Apply these rules:
- Propagate return values: if a lower-level API returns an error/status, return it (or convert it to a documented error code) instead of discarding it.
- Avoid assert/exit in library code: replace `assert(0)`/process termination with a returned error code so the caller can decide how to recover.
- Use consistent error codes: pick and follow conventions (e.g., `-1` for invalid parameter, existing `-100` for allocation failure, etc.).
- Validate shapes with packing and dynamic dims: reject only when the producer/consumer shapes are known-static and truly incompatible; handle dynamic dims (non-positive) and elempack scaling.

Example: propagate and handle submit errors
```cpp
// Bad: ignoring status
cmd.submit_and_wait();
return 0;

// Good: propagate to caller
return cmd.submit_and_wait();
```

Example: avoid assert(0) in library code
```cpp
switch (impl_type) {
    case 1: /* ... */ break;
    case 2: /* ... */ break;
    // ...
    default:
        return -1; // invalid impl_type
}
```