---
title: Enable callback chaining
description: When designing APIs that accept callbacks or configuration functions,
  always return the previous callback/configuration to enable chaining and composition.
  This allows multiple components to layer their functionality without losing existing
  behavior.
repository: ggml-org/llama.cpp
label: API
language: Other
comments_count: 2
repository_stars: 83559
---

When designing APIs that accept callbacks or configuration functions, always return the previous callback/configuration to enable chaining and composition. This allows multiple components to layer their functionality without losing existing behavior.

For callback setters, return the previous callback so callers can chain multiple handlers:

```c
// Good: Returns previous callback for chaining
GGML_API ggml_abort_callback_t ggml_set_abort_callback(ggml_abort_callback_t callback);

// Usage allows chaining:
ggml_abort_callback_t prev_callback = ggml_set_abort_callback(my_callback);
// Can later restore or chain: my_callback can call prev_callback
```

For initialization functions, prefer passing callbacks as parameters rather than extending the API with many specific functions:

```c
// Preferred: Callback-based approach
llama_sampler_init_grammar(grammar_str, grammar_root, is_empty_callback, accept_str_callback);

// Avoid: Function proliferation
llama_sampler_is_grammar_empty(gsmpl);  // Separate function for each operation
```

This approach promotes API composability, reduces function proliferation, and enables multiple components to work together seamlessly.