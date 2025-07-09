---
title: Define explicit error sets
description: Always define explicit error sets for functions that can fail, rather
  than using inferred error sets. This makes error handling more maintainable and
  helps catch missing error cases during development. The error set should be defined
  at the function level, even for simple APIs.
repository: ghostty-org/ghostty
label: Error Handling
language: Other
comments_count: 3
repository_stars: 32864
---

Always define explicit error sets for functions that can fail, rather than using inferred error sets. This makes error handling more maintainable and helps catch missing error cases during development. The error set should be defined at the function level, even for simple APIs.

Example:
```zig
// Instead of:
pub fn init(alloc: Allocator, opts: rendererpkg.Options) !OpenGL {
    // ...
}

// Do this:
const InitError = error{
    OutOfMemory,
    InvalidVersion,
    DeviceNotFound,
};

pub fn init(alloc: Allocator, opts: rendererpkg.Options) InitError!OpenGL {
    // ...
}
```

This approach:
1. Makes all possible errors explicit in the API
2. Helps catch missing error handling during development
3. Improves API documentation
4. Makes it easier to handle specific error cases

Even for wrapper functions or simple APIs, defining the error set helps maintain consistency and makes future modifications safer by forcing explicit consideration of error cases.