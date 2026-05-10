---
title: Hot-Path Performance Rules
description: 'Default to the cheapest behavior: gate expensive work behind explicit
  options or conditions, and keep the parsing “fast path” strictly minimal.


  Practical rules:'
repository: colinhacks/zod
label: Performance Optimization
language: TypeScript
comments_count: 8
repository_stars: 42628
---

Default to the cheapest behavior: gate expensive work behind explicit options or conditions, and keep the parsing “fast path” strictly minimal.

Practical rules:
- Don’t do expensive checks by default (e.g., uniqueness/duplicate detection); make it opt-in or only run when requested.
- Avoid exceptions in hot paths (prefer non-throwing validation branches; don’t rely on `try/catch`/`throw` for normal control flow).
- Minimize allocations on the hot path: only create parsing context/temporary structures when you’re actually going to report an issue.
- Reduce avoidable property access/copies in performance-critical code; avoid repeated computations inside tight loops.
- Use early-exit algorithms when they can reduce average work (and benchmark against alternatives—e.g., `Set` vs double-loop depends on duplicate rates).
- If environment checks are needed (feature detection), do them once via a toggle/initialization strategy—not on every call.

Example pattern (non-throwing, avoid eager ctx/allocation):
```ts
_parse(input: ParseInput) {
  const status = getStatus();

  // Fast path: keep ctx/allocations out unless needed
  if (/* invalid condition */) {
    const ctx = this._getOrReturnCtx(input); // create only now
    addIssueToContext(ctx, { code: '...' });
    status.dirty();
    return status;
  }

  // No try/catch/throw in normal flow
  return status;
}
```

Before/after any performance-sensitive change, run benchmarks or flamegraphs on realistic workloads (include the operations that trigger JIT/fast-pass warmup if relevant).