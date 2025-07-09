---
title: Precise algorithm terminology
description: When implementing and documenting algorithms, use precise terminology
  and be explicit about metrics, operations, and data structures to avoid ambiguity
  and ensure correctness.
repository: neondatabase/neon
label: Algorithms
language: Markdown
comments_count: 3
repository_stars: 19015
---

When implementing and documenting algorithms, use precise terminology and be explicit about metrics, operations, and data structures to avoid ambiguity and ensure correctness.

**Key practices:**

1. **Be explicit about threshold metrics:** Clearly distinguish between counting operations (`count`) versus measuring their size or impact (`sum`). For example:
   ```rust
   // Be specific about threshold conditions
   if count(deltas) < threshold {  // Clear that we're counting operations
       // retain deltas
   } else if sum(delta_sizes) < size_threshold {  // Clear that we're measuring size
       // different logic based on total size
   }
   ```

2. **Use accurate descriptors for data structures:** Choose precise terminology like "sparse" instead of "partial" when describing specialized data structures. This communicates the exact properties and access patterns.

3. **Document algorithmic complexity accurately:** When describing performance characteristics, ensure grammatical accuracy and precision (e.g., "does not have such a constant factor" rather than "does not has").

Proper terminology choices make algorithms easier to understand, maintain, and optimize. They also help prevent subtle bugs that can arise from misinterpreting how an algorithm should behave based on ambiguous descriptions.