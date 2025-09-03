---
title: validate API inputs comprehensively
description: Ensure thorough validation of API inputs and outputs using robust validation
  techniques rather than simple string checks or partial validation. Use proper libraries
  for validation (like urllib.parse for URLs) and validate all required components,
  not just a subset.
repository: langflow-ai/langflow
label: API
language: Python
comments_count: 2
repository_stars: 111046
---

Ensure thorough validation of API inputs and outputs using robust validation techniques rather than simple string checks or partial validation. Use proper libraries for validation (like urllib.parse for URLs) and validate all required components, not just a subset.

For URL validation, avoid simple string prefix checks:
```python
# Avoid this
if source_name.startswith("http"):
    # process URL

# Use this instead
from urllib.parse import urlparse
parsed = urlparse(source_name)
if parsed.scheme in ['http', 'https', 's3', 'gs']:
    # process URL
```

For component validation, ensure completeness:
```python
# Avoid partial validation
if "Chat Input" not in display_names:
    raise ValueError("Missing ChatInput component")

# Validate all required components
required_components = ["Chat Input", "Chat Output"]
missing = [comp for comp in required_components if comp not in display_names]
if missing:
    raise ValueError(f"Missing required components: {missing}")
```

This prevents runtime errors, improves API reliability, and ensures consistent behavior across different input scenarios.