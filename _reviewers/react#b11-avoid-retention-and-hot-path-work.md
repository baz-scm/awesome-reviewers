---
title: Avoid Retention and Hot-Path Work
description: 'Optimize for both runtime speed and heap behavior by (1) preventing
  accidental retention/leaks and (2) keeping critical-path work minimal.


  Apply these rules:'
repository: facebook/react#b11
label: Performance Optimization
language: JavaScript
comments_count: 10
repository_stars: 251894
---

Optimize for both runtime speed and heap behavior by (1) preventing accidental retention/leaks and (2) keeping critical-path work minimal.

Apply these rules:
- **Detach/cleanup anything that can keep objects alive.** If you attach event listeners (e.g., abort signals), remove them when the request reaches a terminal state so the listener doesn’t keep the whole Request reachable.
- **Avoid captured references in long-lived error/abort reasons.** Capturing stacks (or other closures) can retain request-scoped caches and prevent GC under load—ensure the stored reason is “lean” when it could outlive the request.
- **Use native fast paths and avoid allocation-heavy loops in tight code.** Prefer engine-optimized primitives (e.g., `TextDecoder`) over manual chunking/`apply` patterns that create many temporary arrays.
- **Guard before calling expensive logic.** Don’t route every value through large parsers/branch-heavy functions when most inputs can be rejected cheaply first.
- **Defer expensive UI work.** For interactive flows (search/filter), compute matches from a deferred value (and show a pending state if needed) so typing isn’t blocked.
- **Avoid recursion/extra work that can explode under many listeners.** Prefer iterative/state checks (or early state-based dispatch) over recursive wake chains.
- **Be cautious with “approximate” optimizations.** If a fast path relies on assumptions (e.g., byte-length heuristics), verify all serialization/behavior call sites still behave correctly; otherwise rename/limit the optimization to true heuristics.

Example (abort listener cleanup to prevent retention):
```js
export function attachAbortSignal(request, signal) {
  if (signal.aborted) {
    abort(request, signal.reason);
    return;
  }
  function listener() {
    detach();
    abort(request, signal.reason);
  }
  function detach() {
    request.detachAbortSignal = null;
    signal.removeEventListener('abort', listener);
  }
  request.detachAbortSignal = detach;
  signal.addEventListener('abort', listener);
}
```

Code review checks:
- What objects are captured by stored errors/reasons/listeners, and how long do they remain reachable?
- Does the change reduce allocations/CPU on the hot path (or at least defer it)?
- Are “optimizations” safe for all call sites/inputs, or only correct under assumptions?