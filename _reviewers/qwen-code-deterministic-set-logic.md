---
title: Deterministic Set Logic
description: When implementing set-based selection/reconciliation algorithms, ensure
  **(1) deterministic outcomes** and **(2) invariant-preserving persisted state**
  across runs.
repository: QwenLM/qwen-code
label: Algorithms
language: Other
comments_count: 2
repository_stars: 26407
---

When implementing set-based selection/reconciliation algorithms, ensure **(1) deterministic outcomes** and **(2) invariant-preserving persisted state** across runs.

**A. Deterministic tie-breaking (order-independent “argmax”)**
If you pick a “best” owner based on computed scores, explicitly define what happens when scores are equal—do not rely on `Map`/array iteration order.

```js
function pickBestOwner(scores) {
  let best = null;
  let bestScore = -Infinity;
  for (const [owner, score] of scores) {
    if (score > bestScore) {
      best = owner;
      bestScore = score;
    } else if (score === bestScore) {
      // deterministic tie-break (example: lexical)
      if (best === null || owner < best) best = owner;
    }
  }
  return best;
}
```

**B. Persist the canonical desired set (not a derived delta)**
In multi-run reconciliation (markers/comments, requested reviewers, etc.), persisted state must represent the **canonical target**. If you persist a filtered/derived view (e.g., `desired - reviewed`), later runs can lose elements and permanently drift from the intended target.

```js
// Canonical marker persistence: store full desired, not effectiveDesired.
const newMarkerBody = `${MARKER} {"desired":${JSON.stringify([...desired].sort())}} -->`;
```

**Checklist for PRs in this area**
- Equal-score/ equal-priority choices have an explicit, order-independent tie-break.
- Any persisted “desired/current” marker/comment reflects the canonical target set, not an intermediate computation that changes after events (like reviews).
- Marker parsing and drift logic are consistent with what you persisted (so “restore” semantics work reliably across runs).