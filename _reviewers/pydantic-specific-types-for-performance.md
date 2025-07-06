---
title: Specific types for performance
description: Using concrete types instead of abstract container classes in data models
  improves validation performance. More specific types require fewer checks and coercion
  attempts, resulting in faster validation. Additionally, ensure proper model parametrization
  to prevent unnecessary revalidation, which can trigger validators repeatedly.
repository: pydantic/pydantic
label: Performance Optimization
language: Markdown
comments_count: 2
repository_stars: 24377
---

Using concrete types instead of abstract container classes in data models improves validation performance. More specific types require fewer checks and coercion attempts, resulting in faster validation. Additionally, ensure proper model parametrization to prevent unnecessary revalidation, which can trigger validators repeatedly.

For example, prefer:
```python
from pydantic import BaseModel

class Model(BaseModel):
    items: list[str]  # Concrete type
```

Instead of:
```python
from collections.abc import Sequence
from pydantic import BaseModel

class Model(BaseModel):
    items: Sequence[str]  # Abstract type - incurs more validation overhead
```

This optimization is particularly important in performance-sensitive code paths where validation occurs frequently.