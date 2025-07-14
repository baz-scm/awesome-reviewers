---
title: Clean all error paths
description: 'Ensure all error paths properly clean up resources and handle errors
  appropriately. This includes:


  1. Using errdefer for cleanup when allocating resources'
repository: oven-sh/bun
label: Error Handling
language: Other
comments_count: 5
repository_stars: 79093
---

Ensure all error paths properly clean up resources and handle errors appropriately. This includes:

1. Using errdefer for cleanup when allocating resources
2. Checking all possible error paths
3. Properly freeing resources in each error case
4. Ensuring consistent error propagation

Example of proper resource cleanup:

```zig
// Bad - potential resource leak
const data = allocator.alloc(u8, size);
const result = processData(data); // May fail
if (result == .err) return error.ProcessFailed;

// Good - cleanup guaranteed on error
const data = try allocator.alloc(u8, size);
errdefer allocator.free(data);
const result = try processData(data);

// For multiple resources
const key = try allocator.dupe(u8, input_key);
errdefer allocator.free(key);
try map.put(allocator, key, value);
```

Common issues to watch for:
- Missing errdefer after resource allocation
- Incomplete cleanup when multiple resources are allocated
- Early returns that bypass cleanup code
- Inconsistent error handling across different paths

This practice helps prevent resource leaks and ensures robust error handling across all execution paths.