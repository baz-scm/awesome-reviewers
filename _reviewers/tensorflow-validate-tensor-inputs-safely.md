---
title: Validate tensor inputs safely
description: When handling tensor inputs that may contain invalid values, use transformational
  approaches rather than conditional checks. Conditional checks like `if value < 0:`
  may work with scalar values but fail with tensor objects during graph execution.
repository: tensorflow/tensorflow
label: Null Handling
language: Python
comments_count: 3
repository_stars: 190625
---

When handling tensor inputs that may contain invalid values, use transformational approaches rather than conditional checks. Conditional checks like `if value < 0:` may work with scalar values but fail with tensor objects during graph execution.

Instead of raising exceptions based on conditions:

```python
# Not tensor-friendly - may fail during graph execution
if clip_norm < 0:
    raise ValueError('clip_norm should be positive')
```

Use transformations to handle invalid values:

```python
# Tensor-friendly approach
clip_norm = math_ops.maximum(clip_norm, 0)  # Convert negative values to zero
```

For type validations, ensure you check all inputs comprehensively:

```python
# Complete validation for both input and output types
if (not dtype.is_floating and not dtype.is_integer) or (not image.dtype.is_floating and not image.dtype.is_integer):
    raise AttributeError('data type must be either floating point or integer')
```

When implementing such transformations, document the behavior clearly to inform users how edge cases are handled.