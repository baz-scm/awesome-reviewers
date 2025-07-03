---
title: Match algorithms to purpose
description: 'Select algorithmic constructs and control structures that are appropriate
  for the specific task. Common issues include:


  1. Using loops when conditional checks are sufficient'
repository: kubeflow/kubeflow
label: Algorithms
language: Python
comments_count: 2
repository_stars: 15064
---

Select algorithmic constructs and control structures that are appropriate for the specific task. Common issues include:

1. Using loops when conditional checks are sufficient
2. Implementing overly complex traversal patterns for simple data structures
3. Missing edge cases in conditional logic that affect algorithm correctness

For example, replace this inefficient nested loop approach:
```python
# Unnecessarily complex traversal
for condition in conditions:
    for item in condition:
        if "reason" in item:
            # process item
```

With a direct, more efficient approach:
```python
# Simple, appropriate traversal
for condition in conditions:
    if "reason" in condition:
        # process condition directly
```

Similarly, use `if` statements rather than `while` loops when you're only checking a condition once without repeated execution. This improves readability, prevents potential infinite loops, and better expresses the logical intent of your code.
