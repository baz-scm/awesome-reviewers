---
title: implement algorithms correctly
description: Ensure algorithmic implementations use correct patterns, handle edge
  cases gracefully, and avoid silent failures. This includes using proper mathematical
  functions, correct object access methods, and robust error handling for each operation.
repository: stanfordnlp/dspy
label: Algorithms
language: Python
comments_count: 6
repository_stars: 27813
---

Ensure algorithmic implementations use correct patterns, handle edge cases gracefully, and avoid silent failures. This includes using proper mathematical functions, correct object access methods, and robust error handling for each operation.

Key principles:
1. **Use correct mathematical functions**: Choose appropriate functions like `np.log2()` instead of `np.log()` when the algorithm specifically requires base-2 logarithms
2. **Handle edge cases per-item**: Implement try/catch logic for individual items rather than wrapping entire operations to prevent silent corruption
3. **Use proper access patterns**: For enums, use `Status(value)` for value-based lookup instead of `Status[value]` which expects names
4. **Check for required attributes**: Verify object attributes exist before accessing them, especially for dynamic types

Example of robust per-item processing:
```python
def _copy_tools(self, tools):
    copied_tools = []
    for tool in tools:
        try:
            copied_tools.append(copy.deepcopy(tool))
        except Exception as e:
            logger.warning(f"Could not deep copy tool {tool}, using shallow copy: {e}")
            copied_tools.append(copy.copy(tool))
    return copied_tools
```

Example of correct enum handling:
```python
# Correct: restore enum from value
parsed_value = Status(value)  # where value is "in_progress"

# Incorrect: lookup by name when you have value
parsed_value = Status[value]  # throws KeyError
```

This approach prevents algorithmic errors that can lead to silent failures, incorrect results, or runtime exceptions in production code.