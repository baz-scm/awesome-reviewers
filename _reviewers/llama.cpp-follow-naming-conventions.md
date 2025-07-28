---
title: Follow naming conventions
description: Maintain consistency with established naming patterns and conventions
  throughout the codebase. This includes matching enum names with their value prefixes,
  following existing API naming patterns, using consistent variable naming within
  similar contexts, and applying appropriate prefixes to avoid naming conflicts.
repository: ggml-org/llama.cpp
label: Naming Conventions
language: Other
comments_count: 6
repository_stars: 83559
---

Maintain consistency with established naming patterns and conventions throughout the codebase. This includes matching enum names with their value prefixes, following existing API naming patterns, using consistent variable naming within similar contexts, and applying appropriate prefixes to avoid naming conflicts.

Key principles:
- **Enum consistency**: Match enum names with their value prefixes (e.g., `diffusion_alg` for `DIFFUSION_ALG_*` values)
- **API pattern adherence**: Maintain established function naming patterns (e.g., `llama_sampler_init_*` family)
- **Variable consistency**: Use consistent naming within similar contexts (e.g., `api_prefix` instead of `server_prefix` when other variables use `api_*`)
- **Appropriate specificity**: Prefer generic names when functionality isn't specific to one implementation (`LLM_KV_MAMBA_RMS_NORM` instead of `LLM_KV_FALCON_H1_MAMBA_RMS_NORM`)
- **Conflict avoidance**: Add appropriate prefixes to prevent naming collisions (e.g., `GGML_CPU_` prefix for CPU-specific macros)

Example:
```c
// Good: Enum name matches value prefix
enum diffusion_alg {
    DIFFUSION_ALG_ORIGIN       = 0,
    DIFFUSION_ALG_MASKGIT_PLUS = 1,
};

// Bad: Enum name doesn't match value prefix  
enum diffusion_algorithm {
    DIFFUSION_ALG_ORIGIN       = 0,
    DIFFUSION_ALG_MASKGIT_PLUS = 1,
};
```