---
title: measure algorithm performance impact
description: Choose algorithms based on measurable performance benefits rather than
  theoretical complexity advantages. Start with simpler implementations and only adopt
  complex algorithms when they demonstrate clear performance improvements over basic
  approaches.
repository: ggml-org/llama.cpp
label: Algorithms
language: Other
comments_count: 3
repository_stars: 83559
---

Choose algorithms based on measurable performance benefits rather than theoretical complexity advantages. Start with simpler implementations and only adopt complex algorithms when they demonstrate clear performance improvements over basic approaches.

When evaluating algorithmic choices:
- Implement and measure simpler solutions first before adding complexity
- Defer advanced optimizations until basic performance targets are met
- Question whether complex algorithms provide measurable benefits over brute-force approaches
- Prefer deterministic algorithms using integer arithmetic over floating-point approaches when precision and consistency matter

For example, when considering the Aho-Corasick algorithm for multi-pattern string matching: "If we can show that the algorithm improves the performance in a measurable way, then it's ok. If not, we might want to fallback to some simpler brute-force approach." Similarly, when implementing matrix operations, focus on achieving good performance with scalar kernels before adding cooperative matrix optimizations.

This approach ensures that algorithmic complexity is justified by real performance gains rather than theoretical benefits, leading to more maintainable and predictably performing code.