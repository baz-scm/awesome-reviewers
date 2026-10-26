---
title: Bound Complexity Safely
description: When implementing algorithmic logic (parsing, estimation, token/cap calculations,
  archive processing, or runtime heuristics), ensure (1) work and memory are bounded
  for adversarial/large inputs, (2) computed quantities scale with the correct unit
  (not with raw payload size), and (3) pathological behaviors are avoided.
repository: cline/cline#v2
label: Algorithms
language: TypeScript
comments_count: 5
repository_stars: 70861
---

When implementing algorithmic logic (parsing, estimation, token/cap calculations, archive processing, or runtime heuristics), ensure (1) work and memory are bounded for adversarial/large inputs, (2) computed quantities scale with the correct unit (not with raw payload size), and (3) pathological behaviors are avoided.

Practical rules:
- Enforce explicit caps while streaming/iterating (don’t buffer entire inputs just to check size). 
- Ensure estimators/counters don’t “charge” by the wrong dimension (e.g., image base64 byte/char length shouldn’t dominate token estimates).
- Avoid complexity traps: don’t use regex patterns that can backtrack polynomially on long inputs; prefer linear loops.
- Bound iterative expansions and retries (max link expansion/attempts/depth; cap partial-turn loops/degeneracy checks).
- Add invariant tests that assert the intended scaling (e.g., estimate for huge base64 equals estimate for small base64).

Example (estimation invariant + size/cap discipline):
```ts
// Token estimate: payload length must not move the estimate
const base64Big = "A".repeat(500_000);
const base64Small = "A";
const estimate = (data: string) => estimateRequestInputTokens({
  messages: [{ role: "user", content: [{ type: "image", data, mediaType: "image/png" }] }],
});
expect(estimate(base64Big)).toBe(estimate(base64Small));
```

If you follow these, algorithmic code stays correct under edge cases and won’t degrade into excessive CPU/memory or incorrect truncation/retries as inputs grow.