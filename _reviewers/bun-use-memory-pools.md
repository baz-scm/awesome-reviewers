---
title: Use memory pools
description: Reuse memory with buffer pools for temporary allocations instead of creating
  new buffers each time. This reduces memory allocation overhead and improves performance,
  especially for operations that frequently need temporary storage.
repository: oven-sh/bun
label: Performance Optimization
language: Other
comments_count: 5
repository_stars: 79093
---

Reuse memory with buffer pools for temporary allocations instead of creating new buffers each time. This reduces memory allocation overhead and improves performance, especially for operations that frequently need temporary storage.

```zig
// Instead of this:
var link_target_buf: bun.PathBuffer = undefined;

// Use this:
const link_target_buf = bun.PathBufferPool.get();
defer bun.PathBufferPool.put(link_target_buf);
```

Using memory pools for buffers that are only needed temporarily during a function call helps avoid expensive allocation and deallocation cycles. The pattern of getting from a pool and deferring the return ensures the memory is properly recycled without leaking, even if the function returns early through different code paths.