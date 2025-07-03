---
title: API structure balance
description: Maintain a clear separation between resource-specific API handlers and
  common utilities. Resource-specific handlers should remain in their dedicated modules
  to reduce dependencies, while common functionality should be extracted into shared
  helpers for consistency.
repository: kubeflow/kubeflow
label: API
language: Python
comments_count: 2
repository_stars: 15064
---

Maintain a clear separation between resource-specific API handlers and common utilities. Resource-specific handlers should remain in their dedicated modules to reduce dependencies, while common functionality should be extracted into shared helpers for consistency.

Example:
```python
# GOOD: Common helper function in a shared utility file
# components/crud-web-apps/common/backend/kubeflow/kubeflow/crud_backend/helpers.py
def get_age(k8s_object):
    """Return age information in a standardized format for any k8s object."""
    creation_time = dt.datetime.strptime(
        k8s_object["metadata"]["creationTimestamp"], "%Y-%m-%dT%H:%M:%SZ")
    uptime = dt.datetime.now() - creation_time
    return {
        "uptime": str(uptime).split('.')[0],  # Remove microseconds
        "timestamp": creation_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    }

# GOOD: Resource-specific handlers in dedicated modules
# components/model-web-app/backend/app/routes/inference_service.py
def list_inference_services(namespace):
    """Handler specific to InferenceService resources."""
    # Implementation specific to this resource type
```

This approach prevents common code from accumulating resource-specific dependencies while still promoting reuse of utility functions that apply across multiple API endpoints. When designing APIs, always evaluate whether functionality belongs in shared utilities or should remain in resource-specific implementations.
