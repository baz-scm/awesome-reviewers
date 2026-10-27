---
title: Respect React Semantics
description: When changing React-related code, ensure you’re preserving React’s semantic
  contracts (timing, boundaries, and supported patterns). Avoid “escape hatch” approaches
  that can create a brief inconsistent UI, incorrect reconciliation, or incorrect
  server/client usage.
repository: facebook/react#b17
label: React
language: JavaScript
comments_count: 7
repository_stars: 251891
---

When changing React-related code, ensure you’re preserving React’s semantic contracts (timing, boundaries, and supported patterns). Avoid “escape hatch” approaches that can create a brief inconsistent UI, incorrect reconciliation, or incorrect server/client usage.

Apply these rules:
- Don’t derive critical UI/selection state via `useEffect` when it must stay consistent with the current render. If an effect can produce a post-paint frame with stale state, compute/update the selection synchronously during render.
- Fail fast for server-only APIs used in client components (prefer clear errors over silent behavior).
- Model SSR/Flight correctly: use hydration (`hydrateRoot`) instead of client-rendering over SSR output.
- Prefer `use(promise)` for Suspense-like promise consumption; avoid patterns that rely on throwing Promises that are being deprecated.
- Don’t write to refs/state in unsafe ways during render to force updates; keep updates in render/state transitions per React guidance.
- Preserve reconciliation identity for built-ins/lazy wrappers (e.g., don’t swap `elementType` to a built-in type if Lazy wrapper reconciliation depends on it).

Example (avoid effect-based selection thrash):
```js
// BAD: selection lags for one frame when results change
useEffect(() => {
  setSelected(results[index]);
}, [results, index]);

// BETTER: keep selection derived/synced during render
const nextSelected = results[index] ?? null;
// update state in a controlled way during render only if your pattern supports it
// (e.g., compare previous and set during render per existing codebase patterns)
```