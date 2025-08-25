---
title: Verify algorithmic correctness
description: Ensure algorithmic implementations are correct before applying optimizations
  or complex conditional logic. This is especially critical for performance optimizations,
  computational complexity considerations, and batch processing logic where errors
  can have cascading effects.
repository: sgl-project/sglang
label: Algorithms
language: Python
comments_count: 4
repository_stars: 17245
---

Ensure algorithmic implementations are correct before applying optimizations or complex conditional logic. This is especially critical for performance optimizations, computational complexity considerations, and batch processing logic where errors can have cascading effects.

Key practices:
1. **Validate optimization conditions**: Before applying algorithmic optimizations, ensure all prerequisite conditions are met
2. **Analyze computational complexity**: Consider the algorithmic complexity (e.g., O(bs·seq_len^2)) and precision requirements when implementing performance-critical code
3. **Verify batch processing logic**: Ensure state management and control flow are correct in algorithmic processing pipelines
4. **Use precise arithmetic**: Choose appropriate operators (/ vs //) based on the mathematical requirements of the algorithm

Example from the discussions:
```python
# Incorrect: Optimization applied without proper condition checking
if (_is_flashinfer_available and global_server_args_dict["enable_flashinfer_allreduce"]):
    final_hidden_states = flashinfer_allreduce(final_hidden_states)

# Correct: Verify all conditions before applying optimization
if (self.reduce_results and (self.tp_size > 1 or self.ep_size > 1) and
    _is_flashinfer_available and global_server_args_dict["enable_flashinfer_allreduce"]):
    final_hidden_states = flashinfer_allreduce(final_hidden_states)

# Computational complexity consideration with precise arithmetic
current_workload = sum_seq_lens / forward_batch.batch_size * sum_seq_lens  # Use / for mean
```

This approach prevents algorithmic bugs that can lead to incorrect results, performance degradation, or system instability.