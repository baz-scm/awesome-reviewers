---
title: Header hygiene rules
description: 'Keep headers “composition-safe” and minimal. Apply these rules:


  - **Do not define non-inline function implementations in headers.** Put the implementation
  in a `.cpp` file to avoid multiple-definition/linker problems.'
repository: Tencent/ncnn
label: Code Style
language: Other
comments_count: 6
repository_stars: 23205
---

Keep headers “composition-safe” and minimal. Apply these rules:

- **Do not define non-inline function implementations in headers.** Put the implementation in a `.cpp` file to avoid multiple-definition/linker problems.
- **Avoid leaking preprocessor macros from headers.** If a constant/behavior is needed, prefer `constexpr`, `enum`, or an internal-scoped construct rather than a global `#define`.
- **Use correct include discipline.** Remove duplicated includes and avoid unnecessary headers. Ensure all declarations are protected by appropriate header/platform guards.

Example (bad → good):
```cpp
// bad: in header
// foo.h
int gettimeofday_impl(); // ...
int gettimeofday_impl() { return 0; } // implementation in header

// good: in header
// foo.h
int gettimeofday_impl();

// foo.cpp
int gettimeofday_impl() { return 0; }
```

Checklist for changes to `.h` files:
- Are there any **function bodies** (non-`inline`) in the header?
- Are there any **global `#define`** entries?
- Are there **duplicate/unneeded includes**?
- Are declarations properly **guarded** (header guard / platform guard)?