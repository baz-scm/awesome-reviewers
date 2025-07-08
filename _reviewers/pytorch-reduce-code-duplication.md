---
title: Reduce code duplication
description: Eliminate repeated code patterns by using appropriate abstraction techniques.
  This improves readability, reduces maintenance burden, and minimizes the risk of
  inconsistencies when changes are needed.
repository: pytorch/pytorch
label: Code Style
language: C++
comments_count: 3
repository_stars: 91345
---

Eliminate repeated code patterns by using appropriate abstraction techniques. This improves readability, reduces maintenance burden, and minimizes the risk of inconsistencies when changes are needed.

Consider these approaches:

1. **Use templates for similar functions**:
```cpp
// Instead of multiple similar functions like:
bool use_mkldnn_bf16_matmul(...) { ... }
bool use_mkldnn_fp16_matmul(...) { ... }
bool use_mkldnn_bf32_matmul(...) { ... }

// Use a template:
template <typename T>
bool use_mkldnn_matmul(...);
```

2. **Extract repeated logic into helper functions**:
```cpp
// Instead of duplicating checking logic:
if (condition_for_iv) {
  // many lines of validation logic for iv
}
if (condition_for_src_iv) {
  // same validation logic repeated for src_iv
}

// Create a helper function:
void validateIValue(const IValue& iv) {
  // validation logic in one place
}
```

3. **Use modern iteration patterns**:
```cpp
// Instead of manual indexing:
size_t i = 0;
for (const auto& node : graph_->nodes()) {
  LOG(INFO) << "Node #" << i << ": " << node.toString();
  i++;
}

// Use enumerate for cleaner code:
for (const auto&& [i, node] : c10::enumerate(graph_->nodes())) {
  LOG(INFO) << "Node #" << i << ": " << node.toString();
}
```

By consistently applying these patterns, you'll create more maintainable code that's easier to understand and modify.