---
title: Use higher-level iterations
description: When working with multiple sequences that need to be combined, prefer
  higher-level iteration abstractions over nested loops. This improves code readability,
  reduces nesting depth, and helps prevent logical errors when managing multiple iterative
  dimensions.
repository: pytorch/pytorch
label: Algorithms
language: Python
comments_count: 5
repository_stars: 91345
---

When working with multiple sequences that need to be combined, prefer higher-level iteration abstractions over nested loops. This improves code readability, reduces nesting depth, and helps prevent logical errors when managing multiple iterative dimensions.

For example, instead of writing nested loops:
```python
dtypes = [torch.int, torch.long, torch.short]
for count_dtype in dtypes:
    for prob_dtype in dtypes:
        # process with count_dtype and prob_dtype
```

Use `itertools.product` for a cleaner approach:
```python
dtypes = [torch.int, torch.long, torch.short]
for count_dtype, prob_dtype in itertools.product(dtypes, repeat=2):
    # process with count_dtype and prob_dtype
```

Similarly, other Python constructs can simplify iteration patterns:
- Use `enumerate` when you need both index and value
- Use `zip` to iterate through multiple sequences in parallel
- Use comprehensions instead of building collections with loops
- Consider `reversed`, `sorted`, or other builtin functions when applicable

These higher-level abstractions make algorithmic intent more evident and reduce opportunities for off-by-one errors or incorrect nested logic.