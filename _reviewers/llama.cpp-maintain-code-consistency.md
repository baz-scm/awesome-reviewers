---
title: maintain code consistency
description: Always follow the existing code style patterns and conventions found
  in the surrounding codebase rather than introducing new formatting approaches. This
  includes matching brace placement, function organization, and parameter formatting
  styles.
repository: ggml-org/llama.cpp
label: Code Style
language: Other
comments_count: 4
repository_stars: 83559
---

Always follow the existing code style patterns and conventions found in the surrounding codebase rather than introducing new formatting approaches. This includes matching brace placement, function organization, and parameter formatting styles.

For brace placement, match the surrounding code:
```cpp
// If surrounding code uses this style:
enum ggml_opt_optimizer {
    GGML_OPT_ADAM = 0,
    GGML_OPT_SGD  = 1,
};
```

For function organization, group related declarations together:
```cpp
// Keep getters together
GGML_API ggml_opt_context_t ggml_opt_context_init(void);
GGML_API enum ggml_opt_optimizer_type ggml_opt_context_optimizer_type(ggml_opt_context_t);
GGML_API void ggml_opt_context_free(ggml_opt_context_t);
```

For long parameter lists, improve readability by placing each parameter on a new line:
```cpp
void diffusion_generate(
    llama_context * ctx,
    const llama_token * input_tokens,
    llama_token * output_tokens,
    int32_t n_input,
    int32_t max_length,
    struct diffusion_params params,
    int32_t * n_generated);
```

When established patterns exist in the codebase, follow them even if they require some code duplication. Consistency across the codebase is more valuable than eliminating all duplication, as it makes the code more predictable and maintainable for all contributors.