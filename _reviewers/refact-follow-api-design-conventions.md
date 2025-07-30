---
title: Follow API design conventions
description: Ensure API endpoints adhere to established design conventions including
  proper HTTP methods, authorization requirements, and clean route organization. Use
  GET for data retrieval operations and include appropriate authorization headers
  for protected endpoints. Avoid creating unnecessary routers when prefixes can be
  incorporated directly into route...
repository: smallcloudai/refact
label: API
language: Python
comments_count: 2
repository_stars: 3114
---

Ensure API endpoints adhere to established design conventions including proper HTTP methods, authorization requirements, and clean route organization. Use GET for data retrieval operations and include appropriate authorization headers for protected endpoints. Avoid creating unnecessary routers when prefixes can be incorporated directly into route definitions.

For HTTP methods and security:
```python
# Instead of POST for data retrieval
self.add_api_route('/rh-stats', self._rh_stats, methods=["POST"])

# Use GET with authorization
self.add_api_route('/rh-stats', self._rh_stats, methods=["GET"])  # + authorization header
```

For route organization:
```python
# Instead of creating separate routers with prefixes
CAPSRouter(prefix="/v1", ...)

# Incorporate prefix directly into route
self.add_api_route("/v1/completions", self._completions, methods=["POST"])
```

This approach maintains RESTful principles, improves security posture, and simplifies codebase organization by reducing unnecessary abstraction layers.