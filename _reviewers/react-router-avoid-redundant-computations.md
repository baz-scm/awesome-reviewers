---
title: avoid redundant computations
description: Identify and eliminate repeated expensive operations to improve performance.
  Cache computationally expensive objects like regex patterns, API results, or complex
  calculations outside of loops and repeated execution contexts. Implement early exit
  conditions when possible to avoid unnecessary processing.
repository: remix-run/react-router
label: Performance Optimization
language: TypeScript
comments_count: 3
repository_stars: 55270
---

Identify and eliminate repeated expensive operations to improve performance. Cache computationally expensive objects like regex patterns, API results, or complex calculations outside of loops and repeated execution contexts. Implement early exit conditions when possible to avoid unnecessary processing.

Examples of optimization opportunities:
- Move regex compilation outside loops: `const match = segment.match(/^:([\w-]+)(\?)?/)` should have the regex cached
- Cache function results: Track previously computed values in a Set or Map to avoid re-calling expensive functions like `patchRoutesOnMiss`
- Add early bail-out conditions: Check simple conditions first before performing complex iterations or comparisons

Focus on hot paths and frequently executed code where redundant work has the most impact on performance.