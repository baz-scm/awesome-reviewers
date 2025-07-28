---
title: AI parameter organization
description: Ensure proper organization and placement of AI model parameters, hyperparameters,
  and configuration options. Avoid parameter duplication by reusing existing values,
  and place parameters in their logically appropriate structures.
repository: ggml-org/llama.cpp
label: AI
language: Other
comments_count: 5
repository_stars: 83559
---

Ensure proper organization and placement of AI model parameters, hyperparameters, and configuration options. Avoid parameter duplication by reusing existing values, and place parameters in their logically appropriate structures.

Key principles:
- Avoid duplicating parameters that are already available elsewhere in the codebase
- Use existing parameters instead of creating new ones when functionality overlaps
- Place parameters in their conceptually correct locations (e.g., epochs belong with training logic, not optimizer configuration)
- Follow established patterns for parameter organization within the codebase

Example of good practice:
```cpp
// Instead of adding a new parameter:
struct common_params_diffusion {
    int32_t max_length = 512;  // DON'T: create new parameter
};

// Use existing parameter:
// max_length should be removed and the existing n_ubatch parameter should be used instead

// Instead of duplicating available data:
const int n_swa;  // DON'T: duplicate from hparams
// This is already available from the hparams - no need to duplicate it here
```

This practice is especially important in AI model implementations where parameter proliferation can lead to configuration inconsistencies, maintenance overhead, and potential bugs in model behavior. Always check if the functionality you need already exists before introducing new parameters.