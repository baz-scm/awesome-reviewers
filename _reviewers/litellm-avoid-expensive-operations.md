---
title: avoid expensive operations
description: Identify and optimize resource-intensive operations in frequently executed
  code paths. This includes avoiding memory-doubling operations like `copy.deepcopy()`
  on large objects, preventing blocking I/O in async contexts, and eliminating expensive
  debug logging operations.
repository: BerriAI/litellm
label: Performance Optimization
language: Python
comments_count: 5
repository_stars: 28310
---

Identify and optimize resource-intensive operations in frequently executed code paths. This includes avoiding memory-doubling operations like `copy.deepcopy()` on large objects, preventing blocking I/O in async contexts, and eliminating expensive debug logging operations.

Key areas to review:
- **Memory operations**: Avoid deep copying large objects without considering alternatives like in-place modification or streaming
- **Async contexts**: Move blocking operations (file I/O, environment variable reads) to startup initialization rather than request-time execution  
- **Debug logging**: Avoid expensive serialization operations, especially `json.dumps()` on large objects in hot paths
- **Unbounded growth**: Implement limits on data structures to prevent memory leaks

Example from the discussions:
```python
# Problematic - doubles memory usage
redacted_response = copy.deepcopy(response_json)

# Better - consider in-place modification or streaming for large objects
# Or move expensive operations out of request path

# Problematic - blocking I/O in async context
session = ClientSession(trust_env=True)  # Reads files synchronously

# Better - read environment at startup
proxy_settings = get_environment_proxies()  # At startup
session = ClientSession(proxies=proxy_settings)  # At request time
```

Always profile and measure the impact of operations in performance-critical paths, especially when dealing with large data or high-frequency execution.