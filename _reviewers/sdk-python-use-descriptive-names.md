---
title: Use descriptive names
description: Choose names that clearly convey purpose and intent rather than generic
  or ambiguous terms. Names should be specific enough to understand functionality
  without requiring additional context.
repository: strands-agents/sdk-python
label: Naming Conventions
language: Python
comments_count: 19
repository_stars: 4044
---

Choose names that clearly convey purpose and intent rather than generic or ambiguous terms. Names should be specific enough to understand functionality without requiring additional context.

**Avoid generic names:**
- Don't use generic terms like `utils`, `helpers`, or `base` when more specific alternatives exist
- Instead of `class Executor`, use `class ConcurrentExecutor` or `class SequentialExecutor`
- Replace generic file names like `utils.py` with specific names like `validation.py` or `formatting.py`

**Use semantically meaningful names:**
- Method names should clearly indicate their action: `serialize_state()` and `deserialize_state()` instead of ambiguous alternatives
- Variable names should reflect their content: `next_nodes_to_execute` (plural) instead of `next_node_to_execute` when referring to multiple items
- Parameter names should be self-documenting: `timeout` instead of `timeout_seconds` when accepting a `timedelta` object

**Choose appropriate specificity:**
- Be specific enough to avoid confusion: `get_agent_card()` instead of the vague `_discover_agent_card()`
- Balance verbosity with clarity: `name_override` instead of the verbose `agent_facing_tool_name`
- Use domain-specific terminology: `output_type` instead of `structured_output_type` when the context makes "structured" redundant

**Example:**
```python
# Avoid generic names
class Executor:  # Too generic
    pass

# Use descriptive names  
class ConcurrentToolExecutor:  # Clear purpose and scope
    def serialize_state(self) -> dict:  # Clear action
        pass
    
    def get_next_nodes(self) -> list[str]:  # Clear return type
        pass
```

This approach improves code readability and reduces the need for additional documentation to understand component purposes.