---
title: eliminate code duplication
description: Actively identify and eliminate code duplication by extracting common
  patterns into reusable components. When you notice repeated code blocks, similar
  conditional logic, or duplicate class definitions, consolidate them through extraction
  techniques.
repository: sgl-project/sglang
label: Code Style
language: Python
comments_count: 12
repository_stars: 17245
---

Actively identify and eliminate code duplication by extracting common patterns into reusable components. When you notice repeated code blocks, similar conditional logic, or duplicate class definitions, consolidate them through extraction techniques.

Key strategies:
- **Extract repeated conditional patterns**: When you see the same condition checked multiple times, create data structures or helper functions to eliminate repetition
- **Consolidate duplicate classes/functions**: Instead of creating separate classes with similar functionality, extend existing ones or create shared base implementations
- **Move utility functions to appropriate modules**: Place domain-specific utilities in their respective modules (e.g., vision utilities in `vision_utils.py`, general utilities in `utils.py`)
- **Break down complex functions**: Extract logical chunks from long functions into separate, focused functions for better modularity

Example of pattern extraction:
```python
# Before: Repeated conditional logic
global_num_tokens_gpu=(
    self.prefill_global_num_tokens_gpu
    if hasattr(self, "capture_forward_mode")
    and self.capture_forward_mode == ForwardMode.EXTEND
    else self.global_num_tokens_gpu
),
global_num_tokens_for_logprob_gpu=(
    self.prefill_global_num_tokens_for_logprob_gpu
    if hasattr(self, "capture_forward_mode")
    and self.capture_forward_mode == ForwardMode.EXTEND
    else self.global_num_tokens_for_logprob_gpu
),

# After: Extract pattern into data structure
@dataclass
class TokenConfig:
    global_num_tokens_gpu: Tensor
    global_num_tokens_for_logprob_gpu: Tensor

config = prefill_config if self.capture_forward_mode == ForwardMode.EXTEND else default_config
```

This approach improves maintainability, reduces the chance of inconsistencies, and makes the codebase more readable and easier to modify.