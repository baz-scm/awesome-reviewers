---
title: Default None not empty
description: Always use `None` as the default value for optional parameters and class
  attributes instead of empty collections (`[]`, `{}`, `""`) or other mutable defaults.
  This prevents sharing mutable state between instances and makes null checks more
  explicit.
repository: crewaiinc/crewai
label: Null Handling
language: Python
comments_count: 4
repository_stars: 33945
---

Always use `None` as the default value for optional parameters and class attributes instead of empty collections (`[]`, `{}`, `""`) or other mutable defaults. This prevents sharing mutable state between instances and makes null checks more explicit.

Example:
```python
# ❌ Bad - Using mutable defaults
class ToolAdapter:
    original_tools: List[BaseTool] = []  # Shared between instances
    def __init__(self, items: List[str] = []):  # Mutable default
        self.items = items

# ✅ Good - Using None as default
class ToolAdapter:
    def __init__(self):
        self.original_tools: List[BaseTool] = []  # Instance-specific
    
    def process(self, items: Optional[List[str]] = None):
        items = items or []  # Convert None to empty list
        # Process items...
```

This approach:
1. Prevents shared state bugs from mutable defaults
2. Makes optional parameters explicit
3. Forces conscious initialization of collections
4. Enables clear null checking patterns