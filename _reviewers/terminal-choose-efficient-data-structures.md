---
title: Choose efficient data structures
description: Select data structures and types that optimize for both memory usage
  and computational efficiency. Avoid unnecessary copies, use appropriately sized
  types, and consider the performance characteristics of your choices.
repository: microsoft/terminal
label: Algorithms
language: Other
comments_count: 6
repository_stars: 99242
---

Select data structures and types that optimize for both memory usage and computational efficiency. Avoid unnecessary copies, use appropriately sized types, and consider the performance characteristics of your choices.

Key principles:
- Use immutable, shared data structures when possible instead of per-instance copies (e.g., making `_argDescriptors` lazy-initialized constants rather than mutable copies per instance)
- Choose appropriately sized types for your data (e.g., `IndexType` instead of `size_t` for color indices, `char32_t` instead of `int` for character data)
- Avoid wasteful operations like unnecessary vector merging when simpler alternatives exist
- Use containers designed for your use case (`std::vector<int>` for numeric arrays rather than `std::basic_string<int>`)
- Leverage transparent hash/equality types for better lookup performance in hash containers

Example of inefficient vs efficient approach:
```cpp
// Inefficient: Creates new vector every time
std::vector<ArgDescriptor> GetDescriptors() {
    std::vector<ArgDescriptor> merged;
    for (const auto desc : thisArgs) {
        merged.push_back(desc);  // Unnecessary copying
    }
    return merged;
}

// Efficient: Use shared immutable data
static const auto& GetDescriptors() {
    static const auto descriptors = InitializeDescriptors();
    return descriptors;  // Return reference to shared data
}
```

Consider the computational complexity and memory footprint of your data structure choices, especially for frequently accessed or large-scale data.