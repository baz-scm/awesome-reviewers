---
title: Consistent API design
description: 'When designing and modifying APIs, ensure consistency in parameter naming,
  default values, and which functionality is exposed. Each API design decision should:'
repository: huggingface/tokenizers
label: API
language: Other
comments_count: 2
repository_stars: 9868
---

When designing and modifying APIs, ensure consistency in parameter naming, default values, and which functionality is exposed. Each API design decision should:

1. Use parameter names that clearly communicate their purpose and behavior
2. Choose default values that align with expected behavior and maintain backward compatibility
3. Only expose methods and properties with justified use cases
4. Document parameter behavior thoroughly, especially when multiple interpretations are possible

For example, when adding new parameters like in the `truncate` method:

```python
def truncate(self, max_length, stride=0, left=True):
    """Truncate the sequence(s) represented by this encoding
    
    Args:
        max_length: The maximum length to truncate to
        stride: The length of the stride to use
        left: Whether to truncate left (True) or right (False)
    """
    # implementation
```

Ensure the parameter name (`left`) clearly indicates what `True` and `False` values will do, and consider whether the default value matches users' expectations and existing behavior. Document any parameters that might have ambiguous interpretations to prevent confusion.