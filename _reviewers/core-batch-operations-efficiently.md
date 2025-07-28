---
title: Batch operations efficiently
description: Collect and execute similar operations together rather than performing
  them individually to reduce overhead and improve performance. This applies to entity
  creation, API calls, and state updates.
repository: home-assistant/core
label: Performance Optimization
language: Python
comments_count: 4
repository_stars: 80450
---

Collect and execute similar operations together rather than performing them individually to reduce overhead and improve performance. This applies to entity creation, API calls, and state updates.

Key optimization strategies:
1. **Batch entity additions**: Collect all entities during initialization and add them with a single `async_add_entities()` call instead of multiple calls
2. **Combine executor jobs**: Group related synchronous operations into a single executor job to minimize expensive context switching between the event loop and thread pool
3. **Use selective updates**: Choose appropriate update mechanisms - use `async_update_listeners()` when state is already updated locally, or `async_request_refresh()` for buffered updates instead of immediate full refreshes

Example of batching entity creation:
```python
# Instead of multiple calls:
if param_sensors:
    async_add_entities(param_sensors)
if status_sensors:
    async_add_entities(status_sensors)
if alarm_sensors:
    async_add_entities(alarm_sensors)

# Collect all entities and add at once:
all_entities = []
all_entities.extend(param_sensors)
all_entities.extend(status_sensors) 
all_entities.extend(alarm_sensors)
if all_entities:
    async_add_entities(all_entities)
```

This approach reduces function call overhead, improves code clarity, and can significantly improve performance when dealing with large numbers of operations.