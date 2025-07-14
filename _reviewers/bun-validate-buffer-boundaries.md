---
title: Validate buffer boundaries
description: When calling functions that process buffers, especially external C functions,
  always provide explicit buffer size parameters to prevent buffer overflow vulnerabilities.
  Buffer overflows are a common security vulnerability that can lead to memory corruption,
  unauthorized data access, and even remote code execution.
repository: oven-sh/bun
label: Security
language: Other
comments_count: 1
repository_stars: 79093
---

When calling functions that process buffers, especially external C functions, always provide explicit buffer size parameters to prevent buffer overflow vulnerabilities. Buffer overflows are a common security vulnerability that can lead to memory corruption, unauthorized data access, and even remote code execution.

Example (incorrect):
```zig
const res = Bun__writeHTTPDate(buffer, timestampMs);
```

Example (secure):
```zig
const res = Bun__writeHTTPDate(buffer, buffer.len, timestampMs);
```

This is particularly critical for foreign function interface (FFI) calls where the called function may not implement its own buffer boundary checks. Always verify the expected parameters for external functions and ensure buffer lengths are explicitly passed to maintain security boundaries.