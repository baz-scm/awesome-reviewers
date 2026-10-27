---
title: Hot-path allocation discipline
description: In performance-critical code, avoid patterns that create extra allocations/work
  (closures, object spreads/copies, subarrays, per-iteration helper recreation) or
  trigger expensive engine/layout behavior. Prefer native/engine-optimized primitives,
  hoist reusable helpers, and specialize the hottest call paths.
repository: facebook/react#b15
label: Performance Optimization
language: JavaScript
comments_count: 8
repository_stars: 251891
---

In performance-critical code, avoid patterns that create extra allocations/work (closures, object spreads/copies, subarrays, per-iteration helper recreation) or trigger expensive engine/layout behavior. Prefer native/engine-optimized primitives, hoist reusable helpers, and specialize the hottest call paths.

Practical rules:
- Use module-level singletons for expensive/native helpers (e.g., `TextDecoder`) and avoid re-creating them per call.
- Don’t trigger layout/flush work from render/measurement loops (e.g., avoid `getBoundingClientRect` in tight paths).
- Keep hot loops minimal: avoid needless function calls/argument setup when a fast guard can bypass the heavy path.
- Allocate closures/helpers only in the branches that need them; hoist reusable functions to module scope.
- If you need additional behavior in a hot path, fork/specialize instead of adding parameters that change the hottest call site.
- For large data/continuations, avoid repeated tail copying/slicing; consider index-based continuation to prevent churn.
- In per-pass loops, optimize for the common case (check cheap success/fail conditions first) and avoid per-iteration allocations (e.g., prefer scanning over allocating a Set when sizes are expected to be small).

Example (native + no allocation churn):
```js
// module scope
const textDecoderLatin1 = new TextDecoder('latin1');

export function binaryToComparableString(view) {
  // Avoid apply chunking loops; decode in one native call.
  return textDecoderLatin1.decode(new Uint8Array(view.buffer, view.byteOffset, view.byteLength));
}
```

Example (don’t allocate closures unless needed):
```js
function addDebugInfoLater(chunk, streamState) {
  const debugInfoEntry = {awaited: streamState._debugInfo};

  // Only allocate/attach when the async case needs it.
  if (chunk.status === 'pending' || chunk.status === 'blocked') {
    chunk.then(
      () => chunk._debugInfo.push(debugInfoEntry),
      () => {},
    );
  } else {
    chunk._debugInfo.push(debugInfoEntry);
  }
}
```

Apply this by reviewing for hot loops and UI/serialization paths: if it runs often, treat it as “allocation sensitive” and “deopt sensitive,” then benchmark/validate that changes don’t regress other cases.