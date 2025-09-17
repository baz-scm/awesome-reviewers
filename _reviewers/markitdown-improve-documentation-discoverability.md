---
title: Improve documentation discoverability
description: Ensure that important information about code purpose, behavior, and context
  is easily discoverable through proper documentation placement and completeness.
  Add comprehensive docstrings to modules, classes, and functions that explain their
  purpose and usage. Place critical implementation details in docstrings rather than
  inline comments to improve...
repository: microsoft/markitdown
label: Documentation
language: Python
comments_count: 3
repository_stars: 76602
---

Ensure that important information about code purpose, behavior, and context is easily discoverable through proper documentation placement and completeness. Add comprehensive docstrings to modules, classes, and functions that explain their purpose and usage. Place critical implementation details in docstrings rather than inline comments to improve discoverability. Use specific type annotations with clear explanations rather than generic types like `Any`.

For example, instead of:
```python
# Note: We have tight control over the order of built-in converters, but
def __init__(self, markitdown: Any):
    pass
```

Use:
```python
def __init__(self, markitdown: MarkItDown):
    """Initialize converter with MarkItDown instance.
    
    Args:
        markitdown: MarkItDown instance reference to allow recursive 
                   conversions of nested files. We maintain tight control 
                   over the order of built-in converters.
    """
    pass
```

This ensures developers can quickly understand the code's purpose and important implementation details without hunting through comments or guessing from generic type hints.