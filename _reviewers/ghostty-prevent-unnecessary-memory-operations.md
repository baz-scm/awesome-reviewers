---
title: Prevent unnecessary memory operations
description: 'Avoid redundant memory allocations and copies when simpler alternatives
  exist. This includes:


  1. Use in-place comparison functions instead of allocating for string operations'
repository: ghostty-org/ghostty
label: Performance Optimization
language: Other
comments_count: 4
repository_stars: 32864
---

Avoid redundant memory allocations and copies when simpler alternatives exist. This includes:

1. Use in-place comparison functions instead of allocating for string operations
2. Avoid duplicating data that is already owned or will be copied by the receiving function
3. Consider system-specific optimizations to minimize allocations

Example - Instead of:
```zig
const ext_lower = try std.ascii.allocLowerString(alloc, ext);
defer alloc.free(ext_lower);
if (std.mem.eql(u8, ext_lower, ".png")) {
```

Prefer:
```zig
if (std.ascii.eqlIgnoreCase(ext, ".png")) {
```

This guidance helps reduce memory pressure and improve performance by eliminating unnecessary allocations and copies. When working with data structures that handle their own memory management, verify if they copy inputs before performing manual duplication.