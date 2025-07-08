---
title: Parameterize similar test cases
description: Instead of duplicating test code or using nested loops, use test parameterization
  to handle multiple test cases efficiently. This improves maintainability, ensures
  complete coverage, and makes test failures more traceable.
repository: pytorch/pytorch
label: Testing
language: Python
comments_count: 3
repository_stars: 91345
---

Instead of duplicating test code or using nested loops, use test parameterization to handle multiple test cases efficiently. This improves maintainability, ensures complete coverage, and makes test failures more traceable.

Key benefits:
- Reduces code duplication
- Makes test variations explicit
- Easier to add new test cases
- Better failure isolation

Example:
```python
# Instead of:
def test_binomial_dtype_error(self):
    for count_dtype in dtypes:
        for prob_dtype in dtypes:
            # test logic...

# Use:
@parametrize("count_dtype", [torch.int, torch.long, torch.short])
@parametrize("prob_dtype", [torch.int, torch.long, torch.short])
def test_binomial_dtype_error(self, count_dtype, prob_dtype):
    # test logic...

# For multiple configuration parameters:
@parametrize("device", (GPU_TYPE, "cpu"))
@parametrize("format", ("binary", "unpacked"))
@parametrize("dynamic", (False, True))
def test_basic(self, device: str, format: str, dynamic: bool):
    # test logic...
```