---
title: semantic configuration validation
description: When designing configuration systems, prefer semantic parameters over
  generic key-value approaches for common features, and implement runtime validation
  to detect incompatible configuration combinations.
repository: ggml-org/llama.cpp
label: Configurations
language: Other
comments_count: 2
repository_stars: 83559
---

When designing configuration systems, prefer semantic parameters over generic key-value approaches for common features, and implement runtime validation to detect incompatible configuration combinations.

For common functionality, use dedicated semantic variables rather than generic context variables. This maintains a unified API surface and prevents users from needing to learn template-specific idiosyncrasies. When features are incompatible, validate configurations at runtime and provide clear error messages.

Example:
```cpp
// Good: Semantic parameter for common feature
struct config {
    bool enable_thinking = true;
    bool assistant_prefill = false;
};

// Validation with clear error message
if ((!inputs.enable_thinking) || inputs.chat_template_kwargs.find("enable_thinking") != inputs.chat_template_kwargs.end()) {
    throw std::runtime_error("Assistant response prefill is incompatible with enable_thinking.");
}
```

This approach reduces complexity for users while maintaining flexibility for advanced use cases, and prevents runtime failures through proactive validation.