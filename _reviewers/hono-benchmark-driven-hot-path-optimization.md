---
title: Benchmark-driven hot-path optimization
description: For code that executes on every request or in other hot paths (router
  matching, context/response creation, param decoding, JSX stringification, etc.),
  prioritize measured performance over assumed performance, and avoid redundant work.
repository: honojs/Hono
label: Performance Optimization
language: TypeScript
comments_count: 9
repository_stars: 32741
---

For code that executes on every request or in other hot paths (router matching, context/response creation, param decoding, JSX stringification, etc.), prioritize measured performance over assumed performance, and avoid redundant work.

Concretely:
- Before changing a hot-path implementation, benchmark the alternatives (e.g. with `mitata` or simple timing loops) across the runtimes you target (Node, Bun, Deno), since relative performance of built-ins like `.at(-1)` vs `arr[arr.length - 1]`, `in` vs `Object.keys().includes()`, or `new Response()` with/without a `status` option can differ significantly between engines.
- Avoid unnecessary allocations and recomputation: hoist regexes, constants, or other invariants out of functions/loops so they aren't recreated on every call (e.g. compile a regex once at module scope instead of inside a per-item parsing function); avoid extra data copies such as calling `.flat()` unconditionally when most inputs don't need it; prefer native fast paths like `Response.json()` over manual `JSON.stringify` + `new Response` where equivalent.
- Keep cheap fast-path checks (e.g. a quick `/%/`.test()` before an expensive decode, or a `Content-Length` threshold check before compressing) to skip expensive work when it isn't needed, even if it adds a small branch.
- When a "cleaner"/more unified abstraction would introduce extra overhead in a hot path (e.g. merging duplicated logic between JSX attribute builders), it's acceptable to keep the duplicated, specialized, faster implementations instead of a shared but slower one—document the reasoning.
- For code that is not on a hot path (type-level utilities, infrequently-called helpers), prefer readability and simplicity; only micro-optimize when there's a measurable, justified benefit.
- Record the benchmark results (even informally in the PR) when a non-obvious performance trade-off is made, so the rationale is preserved for future readers.

Example: prefer hoisting a regex instead of recompiling it per call:
```ts
// Bad: regex recompiled on every call
const parseAcceptValue = (value: string) => {
  const parts = value.split(/;(?=(?:(?:[^"]*"){2})*[^"]*$)/)
  // ...
}

// Good: regex compiled once
const SPLIT_REGEX = /;(?=(?:(?:[^"]*"){2})*[^"]*$)/
const parseAcceptValue = (value: string) => {
  const parts = value.split(SPLIT_REGEX)
  // ...
}
```