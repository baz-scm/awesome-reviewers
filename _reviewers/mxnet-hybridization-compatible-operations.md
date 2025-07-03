---
title: Hybridization compatible operations
description: When implementing neural network models that will be hybridized for performance
  optimization, use operations that are compatible with symbolic execution to avoid
  runtime errors. Hybridization converts imperative code to symbolic for better inference
  performance, but requires special handling of certain operations.
repository: apache/mxnet
label: AI
language: Python
comments_count: 5
repository_stars: 20801
---

When implementing neural network models that will be hybridized for performance optimization, use operations that are compatible with symbolic execution to avoid runtime errors. Hybridization converts imperative code to symbolic for better inference performance, but requires special handling of certain operations.

Key practices:
1. Replace index operators with slice operations (e.g., use F.slice() instead of [:, :, -x:])
2. Avoid direct references to shape attributes; calculate dimensions explicitly
3. Handle parameter fusion appropriately, especially in RNN layers
4. Test both hybridized and non-hybridized execution paths using parameterized tests

Example of refactoring code for hybridization compatibility:

```python
# NOT compatible with hybridization
def forward(self, x):
    skip_connections = [...]
    output = sum([s[:, :, -output.shape[2]:] for s in skip_connections])
    return output

# Compatible with hybridization
def forward(self, x):
    skip_connections = [...]
    # Option 1: Use F.slice with calculated dimensions
    slice_size = calculate_slice_size(...)  # Calculate based on input size and model params
    output = sum([F.slice(s, begin=(0, 0, -slice_size), end=(None, None, None)) 
                 for s in skip_connections])
    return output
```

When implementing features like callbacks with hybridization, be aware of limitations with static shapes and mark experimental features appropriately in documentation.
