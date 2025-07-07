---
title: Write purposeful comments
description: Comments should explain "why" and "how" rather than restating what is
  already obvious from the code. Focus on providing additional context, usage examples,
  or explanations that would help other developers understand the intent and proper
  usage of the code.
repository: open-telemetry/opentelemetry-python
label: Documentation
language: Python
comments_count: 6
repository_stars: 2061
---

Comments should explain "why" and "how" rather than restating what is already obvious from the code. Focus on providing additional context, usage examples, or explanations that would help other developers understand the intent and proper usage of the code.

**Good practice:**
- Explain complex logic with comments that clarify the purpose
- Document parameter meanings with their expected behavior
- Reference specifications or standards that influenced the implementation
- Clarify how methods should be used in various contexts

**Example - Instead of:**
```python
# Singleton of meter.get_label_set() with zero arguments
```

**Write:**
```python
# This singleton instance is used as the default when no labels are provided,
# avoiding unnecessary object creation during high-frequency metric recording
```

**Example - For complex attribute filtering:**
```python
# Filter out attributes that are already included in point_attributes to avoid
# duplication, keeping only unique attributes from the original measurement
current_attributes = (
    {
        k: v
        for k, v in self.__attributes.items()
        if k not in point_attributes
    }
    if self.__attributes
    else None
)
```

When documenting APIs, be specific about parameter purposes - for example, instead of simply listing "port" and "address" parameters, clarify that they are "the port and address where the service listens for requests from Prometheus."