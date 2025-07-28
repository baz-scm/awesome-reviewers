---
title: validate bounds before access
description: Always validate array indices, buffer sizes, and container bounds before
  accessing elements to prevent out-of-bounds errors and undefined behavior. This
  includes checking that indices are within valid ranges and that containers have
  sufficient size before element access.
repository: ggml-org/llama.cpp
label: Null Handling
language: C++
comments_count: 4
repository_stars: 83559
---

Always validate array indices, buffer sizes, and container bounds before accessing elements to prevent out-of-bounds errors and undefined behavior. This includes checking that indices are within valid ranges and that containers have sufficient size before element access.

Use explicit bounds checking with assertions or conditional statements before array/buffer operations:

```cpp
// Check array bounds before access
GGML_ASSERT(seq_id_src < seq_to_stream.size());
GGML_ASSERT(seq_id_dst < seq_to_stream.size());
const auto s0 = seq_to_stream[seq_id_src];
const auto s1 = seq_to_stream[seq_id_dst];

// Validate string length before character access
if (nextArg.empty() || (nextArg.size() >= 2 && nextArg[0] == '-' && !std::isdigit(nextArg[1]))) {
    // Handle invalid case
}

// Use reserve() and push_back() instead of direct indexing for dynamic arrays
res.idxs.reserve(n_tokens);
// Use push_back() instead of res.idxs[i] = value
```

Consider using safer alternatives like the `.at()` method for containers, which throws exceptions on out-of-bounds access, or implement comprehensive bounds checking at function entry points. This practice prevents memory corruption, crashes, and security vulnerabilities that can arise from accessing invalid memory locations.