---
title: Eliminate code redundancy
description: 'Keep your codebase maintainable by eliminating both unnecessary and
  duplicated code:


  1. **Remove debugging artifacts**: Delete commented-out code, debug print statements,
  and unused imports before merging.'
repository: vllm-project/vllm
label: Code Style
language: Python
comments_count: 11
repository_stars: 51730
---

Keep your codebase maintainable by eliminating both unnecessary and duplicated code:

1. **Remove debugging artifacts**: Delete commented-out code, debug print statements, and unused imports before merging.
   ```python
   # Remove this:
   # print("kv_cache.shape = {}".format(kv_cache.shape))
   
   # And this:
   from vllm.model_executor.layers.activation import get_act_fn  # unused
   ```

2. **Extract duplicated logic** into helper functions or shared classes:
   ```python
   # Instead of this:
   def save_configs(num_experts, ...):
       if enable_expert_parallel:
           filename = get_config_file_name(
               local_num_experts, shard_intermediate_size // 2, 
               dtype_str, block_quant_shape)
       else:
           filename = get_config_file_name(
               num_experts, shard_intermediate_size // 2, 
               dtype_str, block_quant_shape)
               
   # Do this:
   def save_configs(num_experts, ...):
       num_experts_for_filename = (num_experts // ep_size
                                  if enable_expert_parallel else num_experts)
       filename = get_config_file_name(
           num_experts_for_filename, shard_intermediate_size // 2,
           dtype_str, block_quant_shape)
   ```

3. **DRY up similar functionality** when implementing related methods:
   ```python
   # Instead of repeating logic across methods:
   def calculate_metrics(...):
       # Duplicated calculation logic
       
   # Use intermediate variables or helper functions:
   def _calculate_common_part(data):
       # Shared logic extracted here
       
   def calculate_metrics(...):
       result = _calculate_common_part(data)
       # Unique logic continues...
   ```

Eliminate redundancy in all forms - be it duplicate code blocks, methods, imports, or commented-out experimental code that's no longer needed. This makes your code more maintainable, reduces the chance of bugs when changes are needed, and improves readability for other developers.