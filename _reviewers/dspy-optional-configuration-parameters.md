---
title: Optional configuration parameters
description: Make configuration parameters optional with sensible defaults instead
  of requiring mandatory values, and only enable optional features when explicitly
  configured through environment variables or user settings.
repository: stanfordnlp/dspy
label: Configurations
language: Python
comments_count: 6
repository_stars: 27813
---

Make configuration parameters optional with sensible defaults instead of requiring mandatory values, and only enable optional features when explicitly configured through environment variables or user settings.

Many configuration issues arise from rigid parameter requirements that don't accommodate different use cases. Parameters should be optional when they're not always needed, allowing users flexibility while providing sensible defaults for common scenarios.

Key principles:
- Use `Optional[Type] = None` for parameters that aren't always required
- Only enable optional integrations when explicitly configured via environment variables, not just package availability
- Choose defaults that work for majority use cases without causing warnings or errors
- Make hardcoded limits configurable when users have varying needs

Example of flexible configuration:
```python
def __init__(
    self,
    model: str,
    temperature: Optional[float] = None,  # Instead of fixed 0.0
    max_tokens: Optional[int] = None,     # Instead of fixed 1000
    reflection_lm: Optional[LM] = None,   # Optional when using custom proposer
):
    # Set defaults based on model capabilities
    if temperature is None:
        self.temperature = 0.0 if not is_reasoning_model(model) else None
    
    # Only use optional features when explicitly configured
    if reflection_lm is not None:
        with dspy.context(lm=reflection_lm):
            # Use reflection LM
    else:
        # Proceed without reflection LM
```

This approach prevents configuration errors while maintaining backward compatibility and providing users the flexibility they need for different scenarios.