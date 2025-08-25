---
title: Improve code organization
description: Prioritize clean code structure and readability in AI/ML codebases by
  avoiding inline conditionals, using descriptive expressions, and maintaining proper
  separation of concerns. This is especially important in machine learning systems
  where complex logic can quickly become unmaintainable.
repository: sgl-project/sglang
label: AI
language: Python
comments_count: 11
repository_stars: 17245
---

Prioritize clean code structure and readability in AI/ML codebases by avoiding inline conditionals, using descriptive expressions, and maintaining proper separation of concerns. This is especially important in machine learning systems where complex logic can quickly become unmaintainable.

Key practices:
1. **Separate platform-specific logic**: Instead of inline conditionals, create separate functions for different backends or platforms
2. **Use readable expressions**: Replace complex boolean logic with clearer alternatives
3. **Eliminate code duplication**: Extract common patterns into reusable components
4. **Use named constants**: Replace magic numbers with descriptive constants

Example of improved organization:
```python
# Instead of inline conditionals:
if _is_npu:
    # NPU-specific logic here
else:
    # Default logic here

# Use separate functions:
def apply_rotary_pos_emb():
    ...

def apply_rotary_pos_emb_npu():
    ...

if _is_npu:
    apply_rotary_pos_emb = apply_rotary_pos_emb_npu

# Instead of complex conditions:
len(weight_block_size) == 2 or len(weight_block_size) == 1

# Use readable alternatives:
len(weight_block_size) in [1, 2]

# Instead of magic numbers:
TILE_SIZE = 128
BLOCK_SIZE = 4
```

This approach reduces cognitive load, improves maintainability, and makes AI/ML codebases more accessible to team members working across different components.