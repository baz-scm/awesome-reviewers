---
title: Document code thoroughly
description: "Always include comprehensive documentation for your code through both\
  \ docstrings and explanatory comments. \n\nFor classes, functions, and methods,\
  \ add docstrings that explain:"
repository: vllm-project/vllm
label: Documentation
language: Python
comments_count: 10
repository_stars: 51730
---

Always include comprehensive documentation for your code through both docstrings and explanatory comments. 

For classes, functions, and methods, add docstrings that explain:
- The purpose and responsibility of the component
- Parameters with their types, meanings, and constraints
- Return values and their significance
- Special cases or exceptions

For non-obvious implementation details, add comments explaining:
- Why certain approach was chosen
- The reasoning behind workarounds
- Platform-specific behaviors
- Historical context for future maintainers

```python
def uniform_random_select_experts(
    hidden_states: torch.Tensor,
    router_logits: torch.Tensor,
    top_k: int,
    indices_type: Optional[torch.dtype] = None,
) -> tuple[torch.Tensor, torch.Tensor]:
    """Selects experts randomly with uniform distribution instead of based on router scores.
    
    Args:
        hidden_states: Input tensor of shape [batch_size, sequence_length, hidden_size]
        router_logits: Router scores from which only the shape is used
        top_k: Number of experts to select for each token
        indices_type: Optional dtype for the output indices tensor
        
    Returns:
        Tuple containing (routing_weights, expert_indices)
    """
    # CPU only supports V1 architecture due to specialized optimizations
    # that aren't available in the regular implementation
    if current_platform.is_cpu() and os.environ.get("VLLM_USE_V1", "0") == "0":
        pytest.skip("CPU only supports V1")
```

Well-documented code improves maintainability, enables easier onboarding of new team members, and reduces the time needed to understand and modify existing functionality.