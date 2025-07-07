---
title: Handle dynamic shapes
description: When implementing tensor-based algorithms, avoid assumptions about fixed
  tensor shapes by not relying on direct shape attributes (`.shape`, `.ndim`), which
  may return `None` in graph mode. Instead, use TensorFlow operations like `tf.shape()`
  and `tf.rank()` which work in both eager and graph execution modes. For validation,
  use TensorFlow's conditional...
repository: tensorflow/tensorflow
label: Algorithms
language: Python
comments_count: 5
repository_stars: 190625
---

When implementing tensor-based algorithms, avoid assumptions about fixed tensor shapes by not relying on direct shape attributes (`.shape`, `.ndim`), which may return `None` in graph mode. Instead, use TensorFlow operations like `tf.shape()` and `tf.rank()` which work in both eager and graph execution modes. For validation, use TensorFlow's conditional operations rather than Python conditionals.

For example, replace:
```python
# Problematic code - may fail in graph mode
mat1_shape = mat1.shape
dense_rows = mat1_shape[-2]  # This might fail if shape is not known
if dense_shape[-2] != dense_rows:  # Python conditional won't work with tensors
    raise ValueError("Shapes don't match")
```

With:
```python
# Robust code that works in both eager and graph modes
mat1_shape = array_ops.shape(mat1)
dense_rows = mat1_shape[-2]
condition = math_ops.equal(dense_shape[-2], dense_rows)
gen_logging_ops._assert(condition, ["Shapes don't match"], name="Assert")
```

This approach ensures algorithms work reliably regardless of whether shapes are statically known at graph construction time or only determined during execution.