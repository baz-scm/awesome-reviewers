---
title: Configuration default handling
description: Use clean, simple patterns when accessing configuration values with defaults.
  Avoid redundant fallback operations and overly complex boolean conversions that
  reduce code readability.
repository: strands-agents/sdk-python
label: Configurations
language: Python
comments_count: 3
repository_stars: 4044
---

Use clean, simple patterns when accessing configuration values with defaults. Avoid redundant fallback operations and overly complex boolean conversions that reduce code readability.

**Prefer simple .get() with defaults:**
```python
# Good: Clean and readable
"stream": self.config.get("streaming", True)

# Good: Method already returns appropriate default
all_tools_config = self.tool_registry.get_all_tools_config()

# Good: Simple default parameter
session_type: SessionType = SessionType.AGENT
```

**Avoid redundant fallbacks:**
```python
# Avoid: Unnecessary `or {}` when method returns dict
all_tools_config = self.tool_registry.get_all_tools_config() or {}

# Avoid: Overly complex boolean conversion
"stream": bool(self.get_config().get("streaming", True))
```

This pattern improves code maintainability by reducing complexity and making default behavior explicit. When methods already guarantee return types (like returning empty dict), additional fallbacks create confusion about the actual contract. Keep configuration access patterns simple and trust documented method behaviors.