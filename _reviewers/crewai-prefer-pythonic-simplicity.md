---
title: Prefer pythonic simplicity
description: 'Use Python''s expressive features to write cleaner, more maintainable
  code by reducing nesting and improving readability. Follow these practices:


  1. **Avoid unnecessary else blocks** after raising exceptions or returns:'
repository: crewaiinc/crewai
label: Code Style
language: Python
comments_count: 8
repository_stars: 33945
---

Use Python's expressive features to write cleaner, more maintainable code by reducing nesting and improving readability. Follow these practices:

1. **Avoid unnecessary else blocks** after raising exceptions or returns:
```python
# Instead of this:
if not FOUNDRY_AVAILABLE:
    raise ImportError("Foundry Agent Dependencies are not installed.")
else:
    # Do something

# Do this:
if not FOUNDRY_AVAILABLE:
    raise ImportError("Foundry Agent Dependencies are not installed.")
# Do something
```

2. **Use walrus operators** for concise assignment in conditional expressions:
```python
# Instead of this:
knowledge_storage = getattr(agent, "knowledge", None)
if knowledge_storage is not None:
    knowledge_storage.reset()

# Do this:
if (knowledge_storage := getattr(agent, "knowledge", None)) is not None:
    knowledge_storage.reset()
```

3. **Prefer early returns** to reduce indentation and improve readability:
```python
# Instead of nested conditionals:
try:
    for frame_info in stack:
        candidate = frame_info.frame.f_locals.get("self")
        if isinstance(candidate, Flow):
            self.parent_flow = candidate
            break
    else:
        self.parent_flow = None
finally:
    del stack

# Prefer early assignments and returns:
try:
    self.parent_flow = None
    for frame_info in stack:
        candidate = frame_info.frame.f_locals.get("self")
        if isinstance(candidate, Flow):
            self.parent_flow = candidate
            break
    return self   
finally:
    del stack
```

4. **Simplify conditional logic** with default assignments:
```python
# Instead of this:
if not memory_path:
    memory_path = db_storage_path()

# Do this:
memory_path = memory_path or db_storage_path()
```

These practices help reduce cognitive load when reading code and make it easier to spot logical errors. They also lead to more maintainable code by limiting nesting depth and reducing unnecessary verbosity.