---
title: Namespace plugin APIs
description: 'When exposing data to the client, treat shared/global values and plugin
  routes as explicit API surface:


  1) Don’t publish global client/window state by sprinkling ad-hoc dictionaries into
  multiple unrelated API handlers. Instead, use one centralized mechanism:'
repository: agent0ai/agent-zero
label: API
language: Python
comments_count: 4
repository_stars: 17612
---

When exposing data to the client, treat shared/global values and plugin routes as explicit API surface:

1) Don’t publish global client/window state by sprinkling ad-hoc dictionaries into multiple unrelated API handlers. Instead, use one centralized mechanism:
- Inject into `index.html` (e.g., next to `globalThis.gitinfo`), or
- Expose a dedicated “runtime info” endpoint with a stable contract.

Example (centralized injection):
```html
<script>
  // after globalThis.gitinfo
  globalThis.runtimeInfo = {
    isDevelopment: {{ runtime.is_development() | tojson }}
  };
</script>
```

2) Plugin endpoints must be mounted under a stable namespace to prevent collisions with core API routes.
- Route prefix rule: `/plugins/<plugin_name>/...`
- Plugin modules should register their own endpoints under that prefix.

Example (route mounting concept):
```python
# core router bootstrap
register_routes(prefix=f"/plugins/{plugin_name}", handlers=plugin_handlers)
```