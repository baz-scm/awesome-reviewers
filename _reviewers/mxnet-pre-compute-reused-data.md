---
title: Pre-compute reused data
description: When data will be accessed multiple times during processing, avoid redundant
  calculations by pre-computing values upfront rather than using lazy evaluation.
  This pattern significantly improves performance in iterative operations like machine
  learning training, inference, or repeated data transformations.
repository: apache/mxnet
label: Performance Optimization
language: Python
comments_count: 2
repository_stars: 20801
---

When data will be accessed multiple times during processing, avoid redundant calculations by pre-computing values upfront rather than using lazy evaluation. This pattern significantly improves performance in iterative operations like machine learning training, inference, or repeated data transformations.

For example, in data processing pipelines:

```python
# Performance optimization:
# Pre-compute transformations when data will be accessed repeatedly
transformer = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=rgb_mean, std=rgb_std)
])

# Use lazy=False to prepare data upfront when it will be used multiple times
data_loader = DataLoader(dataset.transform_first(transformer, lazy=False))
```

By preparing data once rather than on-demand, you reduce computational overhead and improve overall execution speed, especially in performance-critical sections of code.
