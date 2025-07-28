---
title: API response transformation
description: When integrating external APIs, implement a translation layer that transforms
  responses into a standardized, user-friendly format. This protects consumers from
  upstream API changes and ensures responses are self-documenting without requiring
  external documentation.
repository: home-assistant/core
label: API
language: Other
comments_count: 2
repository_stars: 80450
---

When integrating external APIs, implement a translation layer that transforms responses into a standardized, user-friendly format. This protects consumers from upstream API changes and ensures responses are self-documenting without requiring external documentation.

Key practices:
- Convert field names to snake_case for consistency
- Transform complex data structures into intuitive formats (e.g., duration arrays like [12, 0] into {"hours": 12, "minutes": 0})
- Maintain schema control to prevent breaking changes when external APIs evolve
- Ensure responses are consumable without referring to external API documentation

Example transformation:
```python
# External API response
{
  "programId": 146,
  "duration": [12, 0]  # hours, minutes array
}

# Transformed response
{
  "program_id": 146,
  "duration": {
    "hours": 12,
    "minutes": 0
  }
}
```

This approach ensures automations and integrations remain stable even when external API providers make undocumented changes, while improving the developer experience through clear, self-explanatory data structures.