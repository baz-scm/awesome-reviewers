---
title: Optimize algorithm complexity
description: Choose efficient algorithms and data structures to avoid unnecessary
  computational complexity. Replace manual loops with optimized library functions,
  select appropriate containers based on access patterns, and use direct conversion
  paths when possible.
repository: duckdb/duckdb
label: Algorithms
language: Other
comments_count: 5
repository_stars: 32061
---

Choose efficient algorithms and data structures to avoid unnecessary computational complexity. Replace manual loops with optimized library functions, select appropriate containers based on access patterns, and use direct conversion paths when possible.

Key optimizations to consider:
- Use `memcmp()` instead of character-by-character loops for string comparisons to avoid quadratic complexity
- Add pointer equality short-circuits before expensive comparisons: `if (this_data == other_data) return true;`
- Replace `std::find_first_of()` with simple character checks when scanning for specific characters: `result_offset += c == '\\' || c == '\'';`
- Choose `unordered_map` over `map` when ordering is not required for better lookup performance
- Use direct conversion paths like `std::chrono::duration_cast<std::chrono::microseconds>(time_point.time_since_epoch()).count()` instead of intermediate conversions through `time_t`

Example of string comparison optimization:
```cpp
bool operator==(const String &other) const {
    if (this_size != other_size) return false;
    
    const char *this_data = GetData();
    const char *other_data = other.GetData();
    
    // Short-circuit if same pointer
    if (this_data == other_data) return true;
    
    // Use optimized library function
    return memcmp(this_data, other_data, this_size) == 0;
}
```

Always profile performance-critical code paths and prefer established algorithms over custom implementations when equivalent functionality exists.