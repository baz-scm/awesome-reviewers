---
title: Optimize AI implementation patterns
description: 'When implementing AI systems, prioritize established patterns and optimizations
  rather than creating new implementations for existing problems. This applies to
  all aspects of AI development:'
repository: ollama/ollama
label: AI
language: Other
comments_count: 3
repository_stars: 145705
---

When implementing AI systems, prioritize established patterns and optimizations rather than creating new implementations for existing problems. This applies to all aspects of AI development:

1. For model operations, prefer reusing existing functions over implementing new ones when they serve the same purpose. For example, use `ggml_scale(ctx, cur, -1)` instead of implementing a separate `ggml_neg` operation, as it achieves the same result with equivalent performance and memory usage.

2. When designing data structures for AI models (like vocabulary handling), ensure they account for all possible variations and edge cases. For instance, when handling end-of-generation tokens, remember there may be multiple token types (EOS, EOT) rather than assuming a single one.

3. Maintain precision in documentation of AI tools to ensure clarity for users with different experience levels.

```cpp
// Instead of implementing new operations:
// ggml_tensor * result = ggml_neg(ctx, tensor);

// Prefer reusing existing operations:
ggml_tensor * result = ggml_scale(ctx, tensor, -1);

// Instead of:
struct vocab {
    uint32_t eog_token; // Single end token
};

// Prefer:
struct vocab {
    std::vector<uint32_t> eog_tokens; // Multiple possible end tokens (EOS, EOT)
};
```

These optimizations improve code maintainability, reduce potential bugs, and often lead to better performance in AI systems that already have high computational demands.