---
title: Feature flag gating discipline
description: 'When introducing or modifying feature-flagged behavior, make gating
  consistent, safe to roll out, and predictable across environments.


  Apply these rules:'
repository: facebook/react#b15
label: Configurations
language: JavaScript
comments_count: 9
repository_stars: 251891
---

When introducing or modifying feature-flagged behavior, make gating consistent, safe to roll out, and predictable across environments.

Apply these rules:
1) Roll out safely: if a flag isn’t enabled in OSS yet, enable it everywhere first (so you can quickly disable) before removing or changing defaults.
2) Gate at the correct scope: if a block’s side effects/logging/debugging depend on a flag, guard the entire block—not only the helper call—so behavior is correct and dead code can be eliminated.
3) Prefer implementation-level guards: don’t over-gate at entrypoints just to pass options through; pass/compute as needed and guard the actual usage deeper in the implementation (keep call sites consistent with existing patterns).
4) Keep gating style consistent: use clear, uniform structures like `if (flag) { if (specificCondition) { ... } }` rather than mixed/nested patterns that make reasoning harder.
5) Use the standard test gating mechanism: in tests, prefer `gate('flag')` over importing feature-flag modules.
6) Keep flags present across targets: even if a renderer/feature isn’t used in a given environment, define the flag so removal doesn’t get blocked later.
7) Avoid unnecessary dev-only work: don’t add dev/debug logic to code paths that never run in dev, and ensure dev gating matches intent (e.g., `__DEV__` vs external conditions like DevTools presence).

Example pattern:
```js
// Good: guard the whole block that depends on the flag.
if (enableAsyncDebugInfo) {
  // All debug info side effects here.
  resolveDebugValue(moduleObject == null ? undefined : moduleObject.default);
}

// Good: consistent structure.
if (enableFragmentRefsTextNodes) {
  if (child.tag === HostText) {
    // ...
  }
}
```

Following this keeps feature-flag behavior correct, reduces confusion across builds, and makes future rollouts/removals straightforward.