---
title: avoid internal object access
description: Avoid accessing internal object attributes like `__dict__` or using unpacking
  syntax when cleaner alternatives exist. Instead, prefer stable public methods or
  direct assignment patterns that don't couple to object internals.
repository: langflow-ai/langflow
label: Code Style
language: Python
comments_count: 2
repository_stars: 111046
---

Avoid accessing internal object attributes like `__dict__` or using unpacking syntax when cleaner alternatives exist. Instead, prefer stable public methods or direct assignment patterns that don't couple to object internals.

For object attribute access, use stable methods when available:
```python
# Avoid
"usage": response.usage.__dict__ if hasattr(response, "usage") else None

# Prefer
"usage": response.usage.model_dump() if hasattr(response, "usage") else None
# or explicitly map known fields
"usage": {"tokens": response.usage.tokens, "cost": response.usage.cost} if hasattr(response, "usage") else None
```

For list/tuple assignments, use direct assignment when possible:
```python
# Avoid
outputs = [*BaseFileComponent._base_outputs]

# Prefer  
outputs = BaseFileComponent._base_outputs
```

This approach reduces coupling to implementation details, improves maintainability, and makes code more resilient to internal API changes.