---
title: Vectorize over Python loops
description: Replace Python loops and list comprehensions with vectorized operations
  when processing tensors or performing repeated computations. This optimization reduces
  interpreter overhead and enables efficient parallel execution on modern hardware.
repository: vllm-project/vllm
label: Performance Optimization
language: Python
comments_count: 8
repository_stars: 51730
---

Replace Python loops and list comprehensions with vectorized operations when processing tensors or performing repeated computations. This optimization reduces interpreter overhead and enables efficient parallel execution on modern hardware.

Key practices:
1. Use torch.einsum/matmul for batched matrix operations
2. Leverage torch.gather for indexed tensor operations  
3. Pre-compute and cache frequently accessed values
4. Process data in batches rather than element-by-element

Example - Converting nested loops to vectorized operations:

```python
# Before - Inefficient nested loops
def disentangled_attention_bias(query_layer, key_layer, relative_pos, rel_embeddings):
    content_to_position = torch.zeros_like(content_to_content)
    for i in range(seq_len):
        q_i = query_layer[:, :, i, :]
        for j in range(seq_len):
            rel_idx = relative_pos[i, j].item()
            content_to_position[:, :, i, j] = torch.einsum("bnh,rnh->bnr", 
                                                         q_i, rel_k)[:, :, rel_idx]

# After - Vectorized implementation 
def disentangled_attention_bias(query_layer, key_layer, relative_pos, rel_embeddings):
    c2p_scores = torch.einsum("bnqh,rnh->bnqr", query_layer, rel_k)
    rel_pos_expanded = relative_pos.unsqueeze(0).unsqueeze(0)
    content_to_position = torch.gather(c2p_scores, 3, rel_pos_expanded)
```

This optimization can significantly improve performance by:
- Reducing Python interpreter overhead
- Enabling parallel execution on GPU/TPU
- Minimizing memory allocations
- Leveraging optimized CUDA kernels