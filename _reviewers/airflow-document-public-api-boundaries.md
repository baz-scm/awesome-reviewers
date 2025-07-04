---
title: Document public API boundaries
description: Clearly define and document the boundaries between public and internal
  APIs to guide developers on proper interface usage. Use dedicated namespaces (like
  the 'sdk' namespace) to distinguish public interfaces from internal implementations.
  Ensure all public interfaces have comprehensive documentation that accurately reflects
  behavior, with consistent...
repository: apache/airflow
label: API
language: Other
comments_count: 4
repository_stars: 40858
---

Clearly define and document the boundaries between public and internal APIs to guide developers on proper interface usage. Use dedicated namespaces (like the 'sdk' namespace) to distinguish public interfaces from internal implementations. Ensure all public interfaces have comprehensive documentation that accurately reflects behavior, with consistent terminology across all references.

When creating extension points for your API, document them thoroughly with examples:

```python
# Example of a well-documented API extension point
class AirflowApiExtensionPlugin(AirflowPlugin):
    """Plugin that extends the Airflow API with custom endpoints.
    
    This plugin allows adding FastAPI applications to extend Airflow's API.
    """
    fastapi_apps = [
        {
            "app": app,  # FastAPI app instance
            "url_prefix": "/my-api-extension",  # URL prefix for all endpoints
            "name": "My API Extension",  # Descriptive name shown in UI
        }
    ]
```

For client interfaces, document all available methods, parameters, and expected responses. Include information about error handling, authentication requirements, and rate limiting where applicable. Explicitly state which components are guaranteed to remain stable across versions and which may change, helping developers make informed decisions about API dependencies.