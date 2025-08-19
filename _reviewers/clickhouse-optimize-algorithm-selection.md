---
title: optimize algorithm selection
description: Choose algorithms and data structures based on actual performance characteristics
  rather than defaulting to standard library implementations. Consider lighter-weight
  alternatives when standard library functions are over-engineered for your use case.
repository: ClickHouse/ClickHouse
label: Algorithms
language: Other
comments_count: 5
repository_stars: 42425
---

Choose algorithms and data structures based on actual performance characteristics rather than defaulting to standard library implementations. Consider lighter-weight alternatives when standard library functions are over-engineered for your use case.

Key optimization strategies:

1. **Hash function selection**: Prefer faster hash functions like `UInt128HashCRC32` over STL's heavier default hash implementations when cryptographic security isn't required.

2. **Search algorithm heuristics**: Use linear search for small datasets (typically ≤16 elements) before falling back to binary search, as the overhead of binary search can exceed its benefits for small collections.

3. **Specialized parsing**: Implement template-based parsing functions for specific bases (2, 8, 10, 16) instead of using generic standard library functions like `strtol()` or `sscanf()` when performance is critical.

4. **Selection algorithms**: Use `std::nth_element` for top-k selection problems instead of full sorting when you only need the k smallest/largest elements.

Example of algorithm selection based on size:
```cpp
inline bool containsInPartitionIdsOrEmpty(const PartitionIds & haystack, const String & needle)
{
    if (haystack.empty())
        return true;
    
    // Use linear search for small collections, binary search for larger ones
    if (haystack.size() <= 16)
        return std::find(haystack.begin(), haystack.end(), needle) != haystack.end();
    else
        return std::binary_search(haystack.cbegin(), haystack.cend(), needle);
}
```

Always profile and measure the actual performance impact of algorithm choices in your specific use case, as theoretical complexity doesn't always translate to real-world performance gains.