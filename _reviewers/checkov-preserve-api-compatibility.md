---
title: Preserve API compatibility
description: When modifying existing APIs, function signatures, or return structures,
  always maintain backward compatibility to prevent breaking dependent code. This
  applies to both internal interfaces between components and external API integrations.
repository: bridgecrewio/checkov
label: API
language: Python
comments_count: 4
repository_stars: 7668
---

When modifying existing APIs, function signatures, or return structures, always maintain backward compatibility to prevent breaking dependent code. This applies to both internal interfaces between components and external API integrations.

Key practices:
1. Make new function parameters optional with sensible defaults
2. Support multiple versions of external APIs when needed
3. Maintain consistent return structures or provide migration paths

Example of adding an optional parameter correctly:
```python
# Before
def serialize_to_json(igraph: Graph) -> Dict[str, Any]:
    # implementation

# After - Added parameter is optional
def serialize_to_json(igraph: Graph, absolute_root_folder: str = None) -> Dict[str, Any]:
    # implementation with handling for when absolute_root_folder is None
```

Example of supporting multiple API versions:
```python
def check_azure_container_registry():
    # Support both v2 and v3 attribute paths
    if "retention_policy/enabled" in resource:
        # Handle v2 API format
        return resource["retention_policy/enabled"]
    elif "data_retention_policy/days" in resource:
        # Handle v3 API format
        return resource["data_retention_policy/days"] > 0
    # Handle missing case appropriately
```

When changes to return values are necessary, consider using tuple returns that can be extended while keeping backward position-compatibility, or use dictionaries/objects that can be enhanced without breaking existing code.