---
title: Document AI implementation references
description: When implementing AI algorithms or neural network operations, document
  the sources of specific implementation choices, especially for parameters or techniques
  that might appear arbitrary or unusual at first glance. Include references to established
  AI frameworks, research papers, or model implementations that informed your approach.
repository: deeplearning4j/deeplearning4j
label: AI
language: C++
comments_count: 2
repository_stars: 14036
---

When implementing AI algorithms or neural network operations, document the sources of specific implementation choices, especially for parameters or techniques that might appear arbitrary or unusual at first glance. Include references to established AI frameworks, research papers, or model implementations that informed your approach.

This practice is particularly important for:
1. Magic numbers in neural network operations (like attention masks)
2. Mathematical formulas or equations adapted from specific libraries
3. Parameter choices that deviate from common defaults

**Example:**
```cpp
// Apply mask to attention weights
// Using 1e9 as a large negative value for masked positions,
// consistent with tensor2tensor implementation.
// Note: BERT uses 1e4, GPT-2 uses 1e10
*weights += (*reshapedMask - 1) * 1e9;
```

This documentation helps future developers understand the rationale behind implementation decisions, facilitates accurate debugging, and enables informed modifications when updating the code. It also preserves knowledge about AI model compatibility that might otherwise be lost over time.