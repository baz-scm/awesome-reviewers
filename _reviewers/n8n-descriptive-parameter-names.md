---
title: Descriptive parameter names
description: Use specific, descriptive parameter names for API resources rather than
  generic identifiers. Parameter names should clearly indicate the resource type they
  refer to by using namespaced identifiers (e.g., `userId` instead of `id`). This
  improves API readability, reduces ambiguity in code, and prevents confusion when
  multiple resource types are used in the...
repository: n8n-io/n8n
label: API
language: Yaml
comments_count: 4
repository_stars: 122978
---

Use specific, descriptive parameter names for API resources rather than generic identifiers. Parameter names should clearly indicate the resource type they refer to by using namespaced identifiers (e.g., `userId` instead of `id`). This improves API readability, reduces ambiguity in code, and prevents confusion when multiple resource types are used in the same context.

When designing API endpoints:
- Prefix ID parameters with the resource name (e.g., `credentialId`, `workflowId`)
- Maintain consistent naming patterns across similar resources
- Document parameter naming conventions for your API

For example, instead of:
```yaml
# In users parameter schema
name: id
```

Use:
```yaml
# In users parameter schema
name: userId
```

This practice is especially important in OpenAPI specifications where parameter names directly impact client implementations. Changing parameter names after an API is published can break clients and require comprehensive updates across endpoint definitions, routes, controllers, and documentation.