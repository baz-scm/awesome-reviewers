---
title: Optimize algorithmic complexity
description: Actively identify and eliminate unnecessary computational overhead in
  algorithms, particularly focusing on nested loops and inefficient data operations
  that can significantly impact performance.
repository: neovim/neovim
label: Algorithms
language: Other
comments_count: 3
repository_stars: 91433
---

Actively identify and eliminate unnecessary computational overhead in algorithms, particularly focusing on nested loops and inefficient data operations that can significantly impact performance.

Key areas to review:

1. **Nested Loop Analysis**: Question the necessity of multiple nested loops. As seen in diagnostic processing code, triple-nested loops were "completely unnecessary" and could be eliminated entirely. Always ask: "Can this nesting be reduced or avoided?"

2. **String Building Efficiency**: Avoid repeated string concatenation in loops, which creates O(n²) complexity. Instead, use table-based accumulation:

```lua
-- Inefficient: O(n²) due to string immutability
local result = ''
for char in text do
  result = result .. char  -- Creates new string each time
end

-- Efficient: O(n) using table accumulation
local parts = {}
for char in text do
  table.insert(parts, char)
end
local result = table.concat(parts)
```

3. **Iterator Overhead**: When implementing custom iterators, avoid expensive operations like pack/unpack for multiple return values. Consider the performance implications of each abstraction layer and whether the convenience justifies the overhead.

4. **Algorithmic Alternatives**: Before implementing complex nested logic, research if existing utilities or algorithms can solve the problem more efficiently. For example, reusing proven range-checking logic instead of reimplementing it.

The goal is to maintain code clarity while ensuring algorithms scale appropriately with input size. When in doubt, prefer simpler algorithms with better complexity characteristics over complex optimizations that may introduce bugs.