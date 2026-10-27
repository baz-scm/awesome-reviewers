---
title: Performance First Patterns
description: 'When optimizing for performance, treat both CPU overhead and memory
  retention as first-class.


  - Prefer engine-native/data-model primitives over manual chunking/allocations in
  hot serialization/parsing paths. Also ensure correctness properties (e.g., bijective
  byte↔code-point mapping) when choosing encodings.'
repository: facebook/react#b8
label: Performance Optimization
language: JavaScript
comments_count: 13
repository_stars: 251889
---

When optimizing for performance, treat both CPU overhead and memory retention as first-class.

- Prefer engine-native/data-model primitives over manual chunking/allocations in hot serialization/parsing paths. Also ensure correctness properties (e.g., bijective byte↔code-point mapping) when choosing encodings.
- Make hot-path code allocation-free: avoid per-iteration `subarray`/spread, avoid unnecessary closures created outside conditional branches, and avoid recursion patterns that can stack overflow.
- Avoid VM/JIT deopts where feasible: don’t introduce `try/catch` in tight call sites just to handle unsupported features; avoid deopt-triggering layout/geometry reads that force reflow (`getBoundingClientRect`) in render/loop paths.
- Prevent unbounded memory growth by severing strong reference chains on teardown (while preserving any intentional debug/instrumentation reachability semantics).
- Any heuristic/deduping that trades CPU for memory must be bounded and justified; verify with micro-benchmarks where possible.
- Validate performance changes with targeted regression tests plus real-world repro/profiling (A/B experiments such as `--stack-trace-limit=0`, heap growth under concurrency), not only local reasoning.

Example pattern (native + bounded correctness):
```js
// Avoid String.fromCharCode.apply(largeArray) call-arg limits and per-chunk allocations.
// Use TextDecoder with an encoding that preserves a bijection for comparable binary strings.
const decoder = new TextDecoder('latin1');
export function binaryToComparableString(view) {
  const bytes = new Uint8Array(view.buffer, view.byteOffset, view.byteLength);
  return decoder.decode(bytes); // single pass, native implementation
}
```

Apply these rules consistently across CPU hot paths and memory-sensitive workloads, and back them with profiling evidence when the change impacts retention behavior.