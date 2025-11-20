---
title: Fail fast explicitly
description: Always throw exceptions for error conditions rather than silently failing,
  logging warnings, or attempting fallback behavior that masks underlying problems.
  When encountering unexpected states, missing required data, or configuration errors,
  raise descriptive exceptions immediately rather than continuing execution with degraded
  functionality.
repository: strands-agents/sdk-python
label: Error Handling
language: Python
comments_count: 5
repository_stars: 4044
---

Always throw exceptions for error conditions rather than silently failing, logging warnings, or attempting fallback behavior that masks underlying problems. When encountering unexpected states, missing required data, or configuration errors, raise descriptive exceptions immediately rather than continuing execution with degraded functionality.

This principle prevents bugs from being masked and ensures developers receive clear feedback about problems in their code. Silent failures make debugging difficult and can lead to unexpected behavior in production.

**Examples of what to avoid:**
```python
# Bad: Silent failure with warning
try:
    saved = self.session_manager.read_multi_agent_json()
except Exception as e:
    logger.warning("Skipping resume; failed to load state: %s", e)
    return  # Silently continue without state

# Bad: Fallback that masks the real problem  
def serialize_node_result(self, raw):
    if hasattr(raw, "to_dict"):
        return raw.to_dict()
    # Fallback for strings and other types
    return {"agent_outputs": [str(raw)]}  # Masks unknown types
```

**Preferred approach:**
```python
# Good: Explicit failure with clear message
try:
    saved = self.session_manager.read_multi_agent_json()
except Exception as e:
    raise RuntimeError(f"Failed to load session state: {e}") from e

# Good: Fail fast on unknown types
def serialize_node_result(self, raw):
    if hasattr(raw, "to_dict"):
        return raw.to_dict()
    if isinstance(raw, dict):
        return raw
    raise TypeError(f"Cannot serialize node result of type {type(raw)}")
```

The goal is to make problems visible immediately so they can be addressed rather than allowing them to propagate silently through the system.