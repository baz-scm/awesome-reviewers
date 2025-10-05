---
title: Maintain naming consistency
description: Ensure field names, method names, and identifiers are consistent across
  different contexts including cross-language SDKs, API specifications, and data structures.
  When multiple naming options exist, prioritize alignment with established patterns
  and accurate representation of the underlying functionality or data.
repository: anthropics/claude-agent-sdk-python
label: Naming Conventions
language: Python
comments_count: 2
repository_stars: 2158
---

Ensure field names, method names, and identifiers are consistent across different contexts including cross-language SDKs, API specifications, and data structures. When multiple naming options exist, prioritize alignment with established patterns and accurate representation of the underlying functionality or data.

For cross-platform consistency, align naming conventions between different language implementations:
```python
# Good: Aligns with TypeScript SDK naming
can_use_tool: ToolPermissionCallback | None = None

# Avoid: Inconsistent with other SDK implementations  
tool_permission_callback: ToolPermissionCallback | None = None
```

For API alignment, ensure field names match the actual data structure or API specification:
```python
# Good: Matches actual API field name
total_cost_usd=data["total_cost_usd"]

# Avoid: Mismatched field name
cost_usd=data["cost_usd"]  # when API actually uses "total_cost_usd"
```

Proactively identify naming inconsistencies during code reviews and prioritize fixes that improve overall system coherence.