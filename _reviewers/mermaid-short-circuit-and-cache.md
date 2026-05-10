---
title: Short-circuit and cache
description: 'Optimize performance-sensitive code by eliminating unnecessary work:


  - **Short-circuit expensive calls:** order conditions so cheap checks run first
  and prevent calling costly functions.'
repository: mermaid-js/mermaid
label: Performance Optimization
language: JavaScript
comments_count: 3
repository_stars: 87952
---

Optimize performance-sensitive code by eliminating unnecessary work:

- **Short-circuit expensive calls:** order conditions so cheap checks run first and prevent calling costly functions.
  ```js
  // Prefer cheap value first to avoid extra computation
  const useHtmlLabels = node.useHtmlLabels || getEffectiveHtmlLabels(getConfig());
  ```

- **Cache invariants outside loops:** don’t call configuration/derived getters repeatedly inside `forEach`/`map`/render loops.
  ```js
  const config = getConfig();
  data.nodes.forEach((item) => {
    // use cached config
  });
  ```

- **Centralize heavy transformations & consider lazy loading:** if you add expensive rendering (e.g., KaTeX/FontAwesome label processing), move shared logic into a common utility used by all diagrams, and consider async/lazy loading so the heavy dependency isn’t bundled/initialized for all cases.
  ```js
  // Idea: shared label transform + optional lazy import of heavy lib
  export async function renderMathLabels(input) {
    const { katex } = await import('katex');
    return katex.renderToString(/*...*/);
  }
  ```