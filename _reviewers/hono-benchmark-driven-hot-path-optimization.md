---
title: Benchmark-driven hot path optimization
description: For performance-sensitive code (request/response handling, routing, serialization,
  and other hot paths executed on every request), validate optimization decisions
  with actual benchmarks rather than assumptions, and eliminate redundant work in
  these paths.
repository: honojs/hono
label: Performance Optimization
language: TypeScript
comments_count: 11
repository_stars: 32741
---

For performance-sensitive code (request/response handling, routing, serialization, and other hot paths executed on every request), validate optimization decisions with actual benchmarks rather than assumptions, and eliminate redundant work in these paths.

Concretely:
- Before merging a performance-related change, measure it with tools like `mitata`, runtime-specific benchmarks (Bun/Deno/Node), or built-in profiling, and include the results in the PR. Don't rely on intuition about what's "obviously" faster—measure it (e.g. `.at(-1)` vs `arr[arr.length - 1]`, streaming vs buffered replace, `new Response()` with/without explicit status).
- Avoid recompiling regexes, re-deriving the same value, or re-running expensive checks inside functions that are called per-request. Hoist constant regexes/values to module scope:
  ```ts
  // Bad: regex recompiled on every call
  const parseValue = (value: string) => value.split(/;(?=...)/)

  // Good: regex compiled once
  const SPLIT_REGEX = /;(?=...)/
  const parseValue = (value: string) => value.split(SPLIT_REGEX)
  ```
- Skip unnecessary transformations/decoding when the cheaper path is sufficient (e.g., only decode a param when it actually contains a `%`, reuse `response.text()` instead of parsing to JSON and re-stringifying, use buffered string replace instead of streaming for small/non-streamed bodies).
- Prefer faster built-in APIs when proven faster for the common case (e.g. `Response.json()`), but fall back to the manual path when extra options (custom headers/status) are required.
- Resist introducing shared/common abstractions in hot paths if they add even small per-call overhead; it's acceptable to duplicate small amounts of logic when stringification/serialization performance is critical.
- When adding checks that only pay off in rare cases (e.g., handling very large values, long request durations), weigh whether the added branching/overhead on the common fast path is justified—remove logic that mainly protects against cases that practically never occur in normal request handling.

The goal is to keep per-request overhead minimal in the core framework path while using empirical evidence, not assumption, to decide between alternative implementations.