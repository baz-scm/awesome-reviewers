---
title: Prefer fast-paths and caching
description: 'When performance matters, structure code to avoid unnecessary work:
  (1) keep cheap fast-paths first for short-circuiting, (2) cache expensive global
  lookups (like config) instead of repeatedly calling them, (3) reuse costly parser/services/stateful
  objects, (4) lazy-load heavy dependencies only when required, and (5) remove redundant
  rendering/computation...'
repository: mermaid-js/mermaid
label: Performance Optimization
language: TypeScript
comments_count: 7
repository_stars: 87952
---

When performance matters, structure code to avoid unnecessary work: (1) keep cheap fast-paths first for short-circuiting, (2) cache expensive global lookups (like config) instead of repeatedly calling them, (3) reuse costly parser/services/stateful objects, (4) lazy-load heavy dependencies only when required, and (5) remove redundant rendering/computation that increases output size.

Practical rules:
- Short-circuit with the most likely/cheapest override first.
  ```ts
  // Fast path: user/node override avoids config evaluation
  const useHtmlLabels = node.useHtmlLabels || getEffectiveHtmlLabels(getConfig());
  ```
- Cache `getConfig()` once per function scope.
  ```ts
  const config = getConfig();
  const titleColor = config.themeVariables.titleColor;
  ```
- Don’t recreate expensive parsers/services per call; initialize once and reuse.
- Lazy-import heavy modules only when needed (and ideally only when the input contains the relevant markers).
  ```ts
  if (needsMathML && hasKatex(text)) {
    const katex = await import('katex');
    // ...use katex
  }
  ```
- Avoid generating unnecessary DOM/SVG output; remove recursive logic that “shaves” nothing visually but adds many elements.

These changes reduce CPU time, allocations, and network/module load, improving both runtime responsiveness and load time.