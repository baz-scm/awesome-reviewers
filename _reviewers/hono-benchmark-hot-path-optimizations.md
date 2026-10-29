---
title: Benchmark hot-path optimizations
description: 'For code on frequently executed paths (request handling, routing, serialization,
  middleware), base optimization decisions on actual benchmarks rather than assumptions,
  and avoid introducing redundant work. Concretely:'
repository: HONOJS/HONO
label: Performance Optimization
language: TypeScript
comments_count: 9
repository_stars: 32741
---

For code on frequently executed paths (request handling, routing, serialization, middleware), base optimization decisions on actual benchmarks rather than assumptions, and avoid introducing redundant work. Concretely:

- Measure before and after any performance-motivated change using a tool like `mitata` or `console.time`, and include the comparison in the PR description when the change trades readability/DRYness for speed.
- Hoist invariant computations out of functions that run per-request/per-call. For example, compile regular expressions once at module scope instead of inside a function:
```ts
// Bad: regex is recompiled on every call
const parseValue = (value: string) => value.split(/;(?=(?:(?:[^"]*"){2})*[^"]*$)/)

// Good: regex compiled once
const SPLIT_REGEX = /;(?=(?:(?:[^"]*"){2})*[^"]*$)/
const parseValue = (value: string) => value.split(SPLIT_REGEX)
```
- Avoid unnecessary allocations/branches on the fast path. Prefer cheap guard checks (e.g. `/%/.test(str)` before decoding, `str.includes(...)` before a `replace`) over always running the expensive operation, and prefer constructing objects (e.g. `new Response()`) with the minimal set of options needed.
- It's acceptable to keep similar-looking logic duplicated across call sites (e.g. JSX attribute stringification) rather than unifying it behind a shared abstraction, if sharing it would add branching/argument overhead to a hot loop. Prioritize per-call-site optimization over DRY in these cases.
- When a native/built-in API (e.g. `Response.json()`) is simpler and measurably at least as fast as a hand-rolled equivalent, prefer it.
- Don't touch or "simplify" already-optimized code outside the scope of the current change, especially if it doesn't move the needle or risks regressing a hot path; keep optimization-focused PRs narrowly scoped and justified by data.

The goal is to make performance-sensitive changes deliberate, measured, and scoped to the code that actually executes on every request, rather than guessing or optimizing cold paths at the expense of clarity.