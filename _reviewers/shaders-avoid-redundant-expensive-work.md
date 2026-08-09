---
title: Avoid redundant expensive work
description: For performance-sensitive React code, prevent unnecessary recomputation
  and avoid “clever” micro-optimizations that add complexity without measurable benefit.
repository: paper-design/shaders
label: Performance Optimization
language: TSX
comments_count: 3
repository_stars: 3286
---

For performance-sensitive React code, prevent unnecessary recomputation and avoid “clever” micro-optimizations that add complexity without measurable benefit.

Apply these rules:
1) Gate expensive processing on *value* changes, not prop identity.
   - If a prop is likely to be recreated (new object/array identity on re-render), use a fast deep-equal check (or a derived/stabilized value) to decide whether to re-run costly work (e.g., uniform processing / shader mount updates).

2) Keep performance-related behavior explicit.
   - When gating animation/rendering based on document visibility (or similar), use an obvious branch so the intended behavior is instantly clear to future readers.

3) Don’t add complexity for negligible micro-optimizations.
   - If there’s no clear, measured impact, prefer a simpler, consistent async/internal API over conditional sync/async branching.

Example pattern:
```ts
const uniformsRegistered = useRef<Uniforms | null>(null);

useLayoutEffect(() => {
  const uniformsDidChange =
    !fastDeepEqual(uniformsRegistered.current, uniformsProp);

  if (!uniformsDidChange) return;

  let cancelled = false;
  processUniforms(uniformsProp).then((u) => {
    if (cancelled) return;
    uniformsRegistered.current = uniformsProp;
    // update or create mount...
  });

  return () => { cancelled = true; };
}, [uniformsProp]);

// Explicit visibility gating
const isVisible = typeof window === 'undefined' || !document.hidden;
const effectiveSpeed = isVisible ? speed : 0; // clear intent

// Keep internal async consistent unless benchmarked otherwise
async function processUniforms(uniforms: Uniforms) {
  const processed = /* ... */;
  // If there’s no async work, return directly at the caller level instead of
  // adding conditional async/sync branching inside the helper.
  return processed;
}
```

This reduces wasted GPU/CPU work (reprocessing uniforms, remounting shaders) while keeping the implementation maintainable and trustworthy.