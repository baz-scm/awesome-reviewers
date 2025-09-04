---
title: Complete parameter documentation
description: Ensure all public functions and classes have comprehensive docstrings
  that include parameter descriptions, type hints, return value documentation, and
  references to related implementations. This significantly improves usability by
  helping developers understand how to use APIs correctly and find related code.
repository: stanfordnlp/dspy
label: Documentation
language: Python
comments_count: 7
repository_stars: 27813
---

Ensure all public functions and classes have comprehensive docstrings that include parameter descriptions, type hints, return value documentation, and references to related implementations. This significantly improves usability by helping developers understand how to use APIs correctly and find related code.

Key requirements:
- Add type hints for all parameters (e.g., `Optional[bool]`, `List[str]`)
- Document each parameter with clear descriptions explaining purpose and expected values
- Use standard "Args:" format following Google style guide
- Include references to related implementations or default behaviors
- Document data structure contents (e.g., "dict mapping field names to validation errors")
- Add usage examples when parameters have complex interactions

Example:
```python
def __init__(
    self,
    signature: Type["Signature"], 
    tools: list[Callable], 
    max_iters: Optional[int] = 5
) -> None:
    """
    Initialize the ReAct module for reasoning and acting with tools.
    
    Args:
        signature: The signature defining input and output fields for the module.
        tools: List of functions, callable classes, or dspy.Tool instances available to the agent.
        max_iters: Maximum number of reasoning iterations to perform. Defaults to 5.
        
    Example:
        ```python
        react = dspy.ReAct(signature="question->answer", tools=[get_weather])
        ```
    """
```

This approach helps developers understand APIs without needing to read implementation code, reduces support burden, and improves overall developer experience.