---
title: Centralize configuration constants
description: Store configuration constants, defaults, and environment variable mappings
  in dedicated configuration files rather than duplicating them across the codebase.
  This provides a single source of truth, improves maintainability, and reduces errors
  from inconsistent values.
repository: kubeflow/kubeflow
label: Configurations
language: Python
comments_count: 4
repository_stars: 15064
---

Store configuration constants, defaults, and environment variable mappings in dedicated configuration files rather than duplicating them across the codebase. This provides a single source of truth, improves maintainability, and reduces errors from inconsistent values.

For environment variables with defaults:
```python
# In a central config.py file:
METRICS = bool(os.environ.get("METRICS", False))
BACKEND_MODE = os.environ.get("BACKEND_MODE", BackendMode.PRODUCTION.value)

# In application code:
from config import METRICS, BACKEND_MODE
```

For registry references, version constants, and other configuration mappings:
```python
# In config.py
AWS_REGISTRIES = {
    "jupyter": "public.ecr.aws/j1r0q0g6/jupyter-web-app",
    "volumes": "public.ecr.aws/j1r0q0g6/volumes-web-app",
    # Add more as needed
}

# In application code:
from config import AWS_REGISTRIES
registry = AWS_REGISTRIES["jupyter"]
```

When system-wide defaults are available (like in configmaps), prefer those over hardcoded values to ensure consistency across components.
