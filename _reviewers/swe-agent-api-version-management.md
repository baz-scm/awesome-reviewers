---
title: API version management
description: When integrating with external APIs, explicitly handle version differences
  and use parameterized configurations instead of hardcoded values. Different API
  versions often require different request methods, endpoints, or parameters, so version-specific
  logic should be clearly defined to prevent incorrect API calls.
repository: SWE-agent/SWE-agent
label: API
language: Python
comments_count: 3
repository_stars: 16839
---

When integrating with external APIs, explicitly handle version differences and use parameterized configurations instead of hardcoded values. Different API versions often require different request methods, endpoints, or parameters, so version-specific logic should be clearly defined to prevent incorrect API calls.

Key practices:
- Maintain explicit lists of models/versions that require specific API handling
- Use configuration files with fallback defaults for version-dependent parameters  
- Route requests to appropriate endpoints based on version detection
- Separate test cases for different API versions when they have different interfaces

Example of explicit version handling:
```python
# Good: Explicit version handling
if self.api_model in ["claude-instant", "claude-2", "claude-2.1"]:
    # Use completions.create() for older models
    response = client.completions.create(...)
else:
    # Use messages.create() for Claude-3 family
    response = client.messages.create(...)
```

Example of parameterized configuration:
```python
# Good: Parameterized with fallback
api_version = cfg.get("OPENAI_API_VERSION", "2024-02-01")
self.client = AzureOpenAI(
    api_key=cfg["AZURE_OPENAI_API_KEY"], 
    azure_endpoint=cfg["AZURE_OPENAI_ENDPOINT"], 
    api_version=api_version
)

# Avoid: Hardcoded version
self.client = AzureOpenAI(..., api_version="2024-02-01")
```

This approach prevents API compatibility issues, makes version updates easier to manage, and ensures the correct API interface is used for each version.