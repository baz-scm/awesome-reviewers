---
title: Format lines and comments
description: Ensure all code follows formatting guidelines for readability and consistency.
  Keep lines under 80 characters, splitting longer lines appropriately across multiple
  lines when needed. All comments should be written as complete sentences with proper
  capitalization and ending punctuation.
repository: tensorflow/tensorflow
label: Code Style
language: Python
comments_count: 2
repository_stars: 190625
---

Ensure all code follows formatting guidelines for readability and consistency. Keep lines under 80 characters, splitting longer lines appropriately across multiple lines when needed. All comments should be written as complete sentences with proper capitalization and ending punctuation.

For example, instead of:
```python
# autoparallel optimizer - automatically parallelizes graphs by splitting along the batch dimension
```

Write it as:
```python
# Autoparallel optimizer - Automatically parallelizes graphs by splitting along
# the batch dimension.
```

For longer parameter descriptions in documentation, follow established patterns:
```python
- min_graph_nodes: The minimum number of nodes in a graph to optimizer.
  For smaller graphs, optimization is skipped.
- auto_parallel: Automatically parallelizes graphs by splitting along the batch
  dimension.
```

This improves readability and helps maintain a professional and consistent codebase.