---
title: API minimalism principle
description: Keep APIs minimal by avoiding redundant interfaces and preferring simple
  solutions over complex ones. When adding functionality, first consider extending
  existing functions rather than creating new ones, especially when there's only a
  single use case. Remove unnecessary options and flags to maintain interface simplicity.
repository: ggml-org/llama.cpp
label: API
language: C++
comments_count: 4
repository_stars: 83559
---

Keep APIs minimal by avoiding redundant interfaces and preferring simple solutions over complex ones. When adding functionality, first consider extending existing functions rather than creating new ones, especially when there's only a single use case. Remove unnecessary options and flags to maintain interface simplicity.

Key principles:
- Extend existing functions instead of adding new APIs when there's only one use case
- Remove redundant command-line flags and options that complicate the interface
- Use simple string operations instead of complex formatting when appropriate
- Keep core library APIs minimal - implement convenience wrappers in user code or examples

Example of extending existing API instead of adding new one:
```c
// Instead of adding llama_sampler_accept_str() for one use case:
// AVOID: llama_sampler_accept_str(gsmpl->grmr, trigger.c_str());

// Extend existing function to accept optional initial string:
gsmpl->grmr = llama_sampler_init_grammar(model, grammar_str, "root", trigger.c_str());
```

Example of interface simplification:
```cpp
// Instead of multiple preview flags:
// AVOID: --preview, --preview-count, --detokenize-preview

// Use single flag with sensible defaults:
// PREFER: --preview (shows fixed number of sequences as both tokens and text)
```

This principle ensures APIs remain maintainable, reduce cognitive load for users, and prevent feature bloat while still providing necessary functionality.