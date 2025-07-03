---
title: Consistent naming patterns
description: 'Maintain consistent naming conventions throughout the codebase to enhance
  readability and reduce confusion. This applies to:


  1. **Import aliases**: Use standardized aliases for imported libraries. When working
  with both MXNet''s NumPy and the official NumPy, use ''onp'' for the official NumPy
  to clearly distinguish between them:'
repository: apache/mxnet
label: Naming Conventions
language: Python
comments_count: 7
repository_stars: 20801
---

Maintain consistent naming conventions throughout the codebase to enhance readability and reduce confusion. This applies to:

1. **Import aliases**: Use standardized aliases for imported libraries. When working with both MXNet's NumPy and the official NumPy, use 'onp' for the official NumPy to clearly distinguish between them:
   ```python
   import numpy as onp  # Official NumPy
   from mxnet import np  # MXNet NumPy
   ```

2. **Parameter naming**: Use semantically appropriate parameter names that indicate their purpose. Avoid using 'self' outside of class methods, and prefer descriptive names like 'array' or 'x' for data parameters:
   ```python
   # Good
   def matrix_transpose(x: ndarray, /) -> ndarray:
       # implementation
   
   # Avoid
   def matrix_transpose(self: ndarray, /) -> ndarray:
       # implementation
   ```

3. **Loop variables**: Use descriptive names for loop variables that represent what they iterate over:
   ```python
   # Good
   for key, value in data_shape.items():
       # implementation
   
   # Avoid
   for obj in data_shape:
       # implementation
   ```

4. **Type annotations**: Maintain a consistent style for type annotations throughout the codebase, with explicit type names for parameters and return values.

5. **Related variables**: Use consistent prefixes or suffixes for related variables (e.g., 'running_mean' and 'running_var' instead of mixing 'moving_' and 'running_' prefixes).
