---
title: Avoid magic numbers
description: Replace hardcoded values and magic numbers in AI model code with named
  constants or configuration parameters. This improves maintainability, reduces errors,
  and makes code more adaptable to different model architectures.
repository: vllm-project/vllm
label: AI
language: Python
comments_count: 9
repository_stars: 51730
---

Replace hardcoded values and magic numbers in AI model code with named constants or configuration parameters. This improves maintainability, reduces errors, and makes code more adaptable to different model architectures.

Common issues include hardcoded head dimensions, tensor shapes, and data paths:

```python
# Problematic: Hardcoded head dimensions
prefill_wrapper.plan(
    qo_indptr,
    kv_indptr,
    num_qo_heads,
    num_kv_heads,
    192,  # Magic number for head_dim_qk
    causal=True,
    head_dim_vo=128,  # Another magic number
)

# Better: Use variables from configuration
prefill_wrapper.plan(
    qo_indptr,
    kv_indptr,
    num_qo_heads,
    num_kv_heads,
    head_dim_qk,  
    causal=True,
    head_dim_vo=self.kv_cache_spec.head_size,
)
```

For model parameters, always derive values from configuration objects rather than embedding assumptions in code. When testing, avoid hardcoded paths and dimensions that may not be portable across environments. In multimodal models, be especially careful with tokenization and embedding logic, which should adapt to the model architecture rather than assuming specific token structures.