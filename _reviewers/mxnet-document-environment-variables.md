---
title: Document environment variables
description: All environment variables must be documented in the central env_var.md
  file with clear descriptions of their purpose, acceptable values, and effects. Use
  consistent naming patterns that reflect the subsystem they configure (e.g., MXNET_CUDNN_*,
  MXNET_MKLDNN_*) and avoid introducing new variables when existing ones can serve
  the same purpose.
repository: apache/mxnet
label: Configurations
language: Other
comments_count: 3
repository_stars: 20801
---

All environment variables must be documented in the central env_var.md file with clear descriptions of their purpose, acceptable values, and effects. Use consistent naming patterns that reflect the subsystem they configure (e.g., MXNET_CUDNN_*, MXNET_MKLDNN_*) and avoid introducing new variables when existing ones can serve the same purpose.

Example:
```cpp
// Good - Uses consistent naming and is documented
// In code:
const bool brgemm_disabled = dmlc::GetEnv("MXNET_MKLDNN_DISABLE_BRGEMM_FC", true);

// In docs/static_site/src/pages/api/faq/env_var.md:
// MXNET_MKLDNN_DISABLE_BRGEMM_FC=[true|false] - Disable BRGEMM algorithm in fully connected layers when using MKLDNN backend. Default is true.

// Bad - Introduces new variable without documentation
static bool use_new_dep_engine = dmlc::GetEnv("MXNET_ASYNC_GPU_ENGINE", false);
// Instead, reuse existing variable:
// static bool use_new_dep_engine = (dmlc::GetEnv("MXNET_ENGINE_TYPE", "") == "AsyncGPU");
```

When adding new configuration options:
1. Check if an existing variable can be extended instead of creating a new one
2. Follow the subsystem naming prefix pattern (MXNET_[SUBSYSTEM]_*)
3. Document the variable in env_var.md with its default value and purpose
4. For enum-like options, document all valid values and their effects
