---
name: bun-reviewer
description: "Guidelines for reviewing Bun (JavaScript runtime) code, emphasizing high-performance patterns and rigorous error handling practices."
license: CC-BY-4.0
---

# Bun Code Review Guidelines

## High-Performance Patterns
Bun is designed for speed, so code should utilize patterns that enhance performance. One important practice is reusing memory instead of frequent allocations. For example, Bun uses buffer pools for temporary data – when reviewing code, ensure that functions which need temporary buffers obtain them from a pool and return them when done, rather than allocating new buffers each time[55][56]. The use of `bun.PathBufferPool.get()` and `.put()` (as seen in Bun’s code) is a model case: it significantly reduces GC pressure by recycling memory for short-lived operations[56]. Similarly, encourage branch prediction hints or patterns (in lower-level Bun code or Zig) where applicable – e.g., structuring `if/else` so the likely case is handled first, which can help the CPU’s branch predictor. Also, make use of move semantics or in-place operations (especially in Bun’s Zig or C++ internals) when moving large data, to avoid copies. Code that respects these performance-focused principles will help Bun maintain its speed advantage.

## Explicit Error Handling
Never let errors go unnoticed in Bun’s codebase. If a function or operation might fail, the code should handle it or propagate it – but never silently swallow it[57]. During review, watch for empty catch blocks or error returns that aren’t checked. Bun’s guidelines show several best practices: (1) Log or report errors in non-critical async tasks instead of ignoring them[58][59]. For instance, if an error occurs during a test file search, Bun’s code writes to a debug output channel so the failure is visible to developers[59]. (2) Keep assertions that enforce assumptions – do not remove or disable assertions that check essential preconditions, as they can catch issues early[60]. (3) Always check return values from system calls or library functions; if a function returns an error code or indicator, handle it. For example, if `handle.init(...)` returns a non-zero error code, throw an exception or otherwise signal failure instead of proceeding as if nothing happened[61]. By ensuring errors are surfaced (via exceptions, logs, or propagated up to a global handler), Bun’s runtime becomes more robust and debuggable. Silent failures are unacceptable because they make issues hard to trace[57].
