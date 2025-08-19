---
title: optimize algorithmic complexity
description: Always consider the algorithmic complexity and performance implications
  of data structure choices, memory allocation patterns, and container operations.
  This includes pre-allocating containers when sizes are known, choosing appropriate
  data structures based on usage patterns, and measuring performance impact of changes.
repository: ClickHouse/ClickHouse
label: Algorithms
language: C++
comments_count: 5
repository_stars: 42425
---

Always consider the algorithmic complexity and performance implications of data structure choices, memory allocation patterns, and container operations. This includes pre-allocating containers when sizes are known, choosing appropriate data structures based on usage patterns, and measuring performance impact of changes.

Key practices:
1. **Pre-allocate containers**: Reserve memory when the final size is predictable to avoid repeated reallocations
2. **Choose containers wisely**: Consider trade-offs between different data structures (e.g., `std::vector` vs `std::unordered_set` vs `std::set`) based on access patterns, insertion frequency, and memory constraints
3. **Size buffers defensively**: When working with external libraries that require "big enough" buffers, add safety margins (e.g., +20%) to prevent overflows
4. **Benchmark performance changes**: Always measure performance impact when modifying algorithms, especially for hot paths

Example of good practice:
```cpp
// Pre-allocate when size is known
structure_granule.all_paths.reserve(structure_granule.num_paths);

// Choose appropriate container based on usage
// For frequent lookups with few duplicates: std::unordered_set
// For ordered iteration: std::set  
// For simple iteration: std::vector
constexpr size_t initial_size_degree = 9; // Conservative default for hash tables
ClearableHashSetWithStackMemory<ValueType, DefaultHash<ValueType>, initial_size_degree> set;

// Size buffers defensively for external libraries
PaddedPODArray<UInt32> compressed_buffer(uncompressed_size * 1.2); // +20% safety margin
```

This approach prevents performance regressions, reduces memory fragmentation, and ensures predictable behavior under different load conditions.