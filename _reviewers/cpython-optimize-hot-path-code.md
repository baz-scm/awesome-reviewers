---
title: Optimize hot-path code
description: In performance-sensitive code (loops, frequently-called functions, parsers,
  I/O paths), eliminate redundant work and unnecessary indirection, and validate optimizations
  with measurements rather than assumptions.
repository: python/cpython
label: Performance Optimization
language: Python
comments_count: 5
repository_stars: 77696
---

In performance-sensitive code (loops, frequently-called functions, parsers, I/O paths), eliminate redundant work and unnecessary indirection, and validate optimizations with measurements rather than assumptions.

Concretely:
- Hoist loop-invariant computations out of loops. For example, precompute masks/constants once before a loop instead of recalculating them on every iteration (e.g. `mask = self._EVENT_READ | self._EVENT_WRITE` computed once outside `for fd, event in fd_event_list:` rather than inside it).
- Avoid creating redundant intermediate objects. If you already hold a `memoryview`, slice it directly instead of wrapping it in another `memoryview` first (`buffer.appendleft(b[nbytes:])` when `b` is already a memoryview, instead of `memoryview(b)[nbytes:]`).
- When adding a "fast path" for a common case, make it as broad and efficient as reasonable without sacrificing correctness, e.g. covering `utf-8`/`utf8` encodings generally rather than only ASCII-only strings, so more real-world inputs benefit from the speedup.
- Be wary of replacing simple, allocation-free control flow (e.g. a `try/except` loop) with higher-level abstractions (e.g. generic `iter()` helpers) purely for readability—if the common/fast path is hit almost every time, extra setup (method binding, exception-type checks, iterator protocol) can measurably regress performance (a reported 40% slowdown in one case). Prefer the implementation that keeps the hot/common path cheap, and benchmark before merging such changes.
- Limit unnecessary symbol exposure in compiled/generated code (e.g. mark internal C functions `Py_LOCAL_SYMBOL`/`static` instead of exporting them). Unneeded exported symbols can force calls through the PLT instead of direct calls, add linker overhead, and risk symbol interposition between independently built modules.

Always back performance-related changes with profiling or benchmark data when the modification affects a hot path, and prefer the version with the least overhead for the most frequently executed case.