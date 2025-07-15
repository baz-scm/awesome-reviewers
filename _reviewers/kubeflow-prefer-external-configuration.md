---
title: Prefer external configuration
description: Design applications to use external configuration sources rather than
  hardcoding values directly in source code. This allows for configuration changes
  without requiring code modifications or redeployment.
repository: kubeflow/kubeflow
label: Configurations
language: JavaScript
comments_count: 2
repository_stars: 15064
---

Design applications to use external configuration sources rather than hardcoding values directly in source code. This allows for configuration changes without requiring code modifications or redeployment.

When defining configurations that might change between environments or user preferences:
- Use mechanisms like ConfigMaps, environment variables, or properly namespaced storage keys
- Consider future extensibility in configuration design
- Prefer dynamic configuration that can be updated without code changes

For example, instead of hardcoding allowed namespaces:
```javascript
// Avoid this
export const ALL_NAMESPACES_ALLOWED_LIST = ['jupyter'];

// Prefer dynamic configuration loaded from an external source
export const ALL_NAMESPACES_ALLOWED_LIST = loadFromConfigMap('namespaces.allowed');
```

Similarly, when importing resources to support configurable features, consider importing complete libraries if it enables easier configuration through external sources:
```javascript
// This allows for configurable icons via ConfigMap without source code changes
import '@polymer/iron-icons/communication-icons.js';
```
