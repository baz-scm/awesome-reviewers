---
title: explicit control flow logic
description: Use explicit control flow structures like switch statements instead of
  complex boolean logic or implicit reasoning when handling algorithmic decisions.
  This improves code clarity, maintainability, and reduces the likelihood of logical
  errors in computational paths.
repository: ggml-org/llama.cpp
label: Algorithms
language: C++
comments_count: 6
repository_stars: 83559
---

Use explicit control flow structures like switch statements instead of complex boolean logic or implicit reasoning when handling algorithmic decisions. This improves code clarity, maintainability, and reduces the likelihood of logical errors in computational paths.

Key principles:
- Replace complex boolean conditions with explicit switch statements when dealing with enumerated types or distinct algorithmic paths
- Maintain consistent state throughout algorithm execution rather than allowing state changes mid-process
- Separate different algorithmic concerns (e.g., buffer allocation vs gradient accumulation logic)
- Ensure algorithmic compatibility constraints are explicitly validated (e.g., sequence independence in batch processing)

Example of preferred approach:
```cpp
// Instead of implicit boolean reasoning:
struct ggml_tensor * opt_step = 
    m ? ggml_opt_step_adamw(ctx, node, grad, m, v, params) :
        ggml_opt_step_sgd(ctx, node, grad, params);

// Use explicit switch statement:
struct ggml_tensor * opt_step;
switch (opt_ctx->optimizer_type) {
    case GGML_OPT_OPTIMIZER_ADAMW:
        opt_step = ggml_opt_step_adamw(ctx, node, grad, m, v, params);
        break;
    case GGML_OPT_OPTIMIZER_SGD:
        opt_step = ggml_opt_step_sgd(ctx, node, grad, params);
        break;
    default:
        GGML_ABORT("fatal error");
        break;
}
```

This approach makes algorithmic decisions explicit, improves debugging, and ensures all code paths are properly handled. It also prevents mixing of unrelated algorithmic concerns and maintains clearer separation of computational logic.