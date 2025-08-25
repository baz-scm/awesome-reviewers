---
title: Explicit API parameters
description: API functions should use explicit parameters rather than passing large
  opaque objects. When a function needs specific data from a complex object, extract
  and pass only the required fields as individual parameters. This makes the function's
  dependencies clear, improves testability, and reduces coupling.
repository: sgl-project/sglang
label: API
language: Python
comments_count: 3
repository_stars: 17245
---

API functions should use explicit parameters rather than passing large opaque objects. When a function needs specific data from a complex object, extract and pass only the required fields as individual parameters. This makes the function's dependencies clear, improves testability, and reduces coupling.

Avoid passing entire objects when only specific fields are needed:

```python
# Bad: Opaque object passing
def forward(
    self,
    hidden_states: torch.Tensor,
    topk_output: StandardTopKOutput,
    forward_batch: Optional[ForwardBatch] = None,  # Unclear what fields are used
):

# Good: Explicit parameters
def forward(
    self,
    hidden_states: torch.Tensor,
    topk_output: StandardTopKOutput,
    dp_padding_mode: bool,
    batch_size: int,
    gathered_buffer: torch.Tensor,
    global_num_tokens: int,
):
```

This approach makes function interfaces self-documenting and prevents unnecessary dependencies on large data structures. If many parameters are needed, consider if the function has too many responsibilities and should be refactored.