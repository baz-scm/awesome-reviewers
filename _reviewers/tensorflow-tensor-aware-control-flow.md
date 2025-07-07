---
title: Tensor-aware control flow
description: When working with TensorFlow tensors, avoid using Python comparison operators
  (`<`, `>=`, `==`) or conditional checks that expect Boolean scalars. Python operators
  evaluate eagerly and won't work correctly with tensors that represent deferred computations.
repository: tensorflow/tensorflow
label: AI
language: Python
comments_count: 4
repository_stars: 190625
---

When working with TensorFlow tensors, avoid using Python comparison operators (`<`, `>=`, `==`) or conditional checks that expect Boolean scalars. Python operators evaluate eagerly and won't work correctly with tensors that represent deferred computations.

Instead:
1. Use TensorFlow's conditional operations like `tf.cond`
2. Use comparison functions from `check_ops` module such as `assert_less`
3. Use TensorFlow's mathematical operations for comparisons

**Incorrect:**
```python
def random_uniform(shape, minval=0, maxval=None, dtype=dtypes.float32):
  if minval >= maxval:  # Will fail if these are tensors
    raise ValueError("minval must be less than maxval")
```

**Correct:**
```python
def random_uniform(shape, minval=0, maxval=None, dtype=dtypes.float32):
  # Use check_ops for tensor-compatible validation
  minval = ops.convert_to_tensor(minval, dtype=dtype)
  maxval = ops.convert_to_tensor(maxval, dtype=dtype)
  check_ops.assert_less(minval, maxval, 
                        message="minval must be less than maxval")
```

This pattern is essential for building TensorFlow graphs that will execute correctly in both eager and graph execution modes, ensuring your AI models behave as expected regardless of execution environment.