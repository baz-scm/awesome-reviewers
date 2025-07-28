---
title: explicit null handling strategies
description: 'Functions and APIs should employ explicit strategies for handling null/None
  values rather than leaving null handling ambiguous. Choose one of two approaches:'
repository: comfyanonymous/ComfyUI
label: Null Handling
language: Python
comments_count: 4
repository_stars: 83726
---

Functions and APIs should employ explicit strategies for handling null/None values rather than leaving null handling ambiguous. Choose one of two approaches:

1. **Design out nulls**: Use sentinel values, default objects, or consistent data structures to eliminate the need for null checks
2. **Explicit null contracts**: If a function can return None, either document that all callers must handle None, or raise an exception instead

**Avoid**: Returning None from functions without clear handling expectations, or requiring frequent isinstance/null checks due to inconsistent data formats.

**Example of good null handling:**
```python
# Option 1: Design out nulls with defaults
def get_config(key: str) -> Config:
    return config_dict.get(key, DEFAULT_CONFIG)  # Never returns None

# Option 2: Explicit null contract  
def get_node(node_id: str) -> Node:
    node = self._find_node(node_id)
    if node is None:
        raise NodeNotFoundError(f"Node {node_id} not found")
    return node
```

**Example of problematic null handling:**
```python
# Ambiguous - callers don't know if they need to handle None
def get_node(node_id: str) -> Node | None:
    # Returns None sometimes, unclear when
    return self.nodes.get(node_id)
```

This approach prevents attribute errors, reduces defensive programming overhead, and makes null-handling expectations explicit in the codebase.