---
title: Optimize data structures
description: Choose appropriate built-in data structures and collection types to improve
  code efficiency and readability. Python's collections module and built-in data structures
  often provide more elegant and performant solutions than manual implementations.
repository: langgenius/dify
label: Algorithms
language: Python
comments_count: 3
repository_stars: 114231
---

Choose appropriate built-in data structures and collection types to improve code efficiency and readability. Python's collections module and built-in data structures often provide more elegant and performant solutions than manual implementations.

Key guidelines:
- Use `collections.UserDict` instead of inheriting from `dict` when you need to override dictionary behavior
- Use `collections.defaultdict` to eliminate manual key existence checks and initialization
- Leverage dictionary comprehensions for deduplication and data transformation tasks

Examples:

```python
# Instead of manual dictionary building:
target_nodes: dict[str, list[GraphEdge]] = {}
for edge in edge_mappings:
    if edge.target_node_id not in target_nodes:
        target_nodes[edge.target_node_id] = []
    target_nodes[edge.target_node_id].append(edge)

# Use defaultdict:
from collections import defaultdict
target_nodes = defaultdict(list)
for edge in edge_mappings:
    target_nodes[edge.target_node_id].append(edge)

# For deduplication, instead of manual loop:
unique_documents = []
doc_ids = set()
for document in documents:
    if document.metadata["doc_id"] not in doc_ids:
        doc_ids.add(document.metadata["doc_id"])
        unique_documents.append(document)

# Use dictionary comprehension:
unique_documents = list({doc.metadata["doc_id"]: doc for doc in documents}.values())
```

These optimizations reduce code complexity, improve performance, and make intent clearer to other developers.