---
title: SDK-aware API clients
description: 'When building or calling API client code, follow the SDK’s actual request/response
  types and conventions instead of assuming REST/dict semantics.


  Apply these rules:'
repository: TauricResearch/TradingAgents
label: API
language: Python
comments_count: 3
repository_stars: 71953
---

When building or calling API client code, follow the SDK’s actual request/response types and conventions instead of assuming REST/dict semantics.

Apply these rules:
- **Respect SDK object models**: If a method constructs a typed proto/object (e.g., `GenerateContentRequest`), access fields using the proto/object APIs (e.g., `request.contents`) rather than dict helpers like `.get()`. This avoids runtime errors and preserves correct request shaping.
- **Avoid hardcoding API version paths**: Don’t blindly append `"/v1"` or force versioned endpoints when the SDK manages its own endpoint construction. Prefer passing `base_url=None` (or the SDK default) so internal path logic remains correct.
- **Keep interface/parameter consistency**: For API-like wrappers, maintain consistent function signatures/parameters (e.g., include `limit` where related functions accept it), so callers have a stable contract across providers.

Example (proto field access + SDK-managed endpoint):
```python
from typing import Any

# Assume `request` is a proto/typed object created by the SDK
def inject_fields(request: Any) -> Any:
    # Proto repeated composite field: iterate directly; do not use request.get(...)
    for content in request.contents:
        for part in content.parts:
            # mutate request parts as required by the API
            pass
    return request

# When initializing provider clients, let the SDK handle endpoint construction
base_url = None  # e.g., instead of hardcoding /v1
```