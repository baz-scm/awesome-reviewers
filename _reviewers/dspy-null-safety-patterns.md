---
title: Null safety patterns
description: 'Implement proper null safety patterns to prevent runtime errors and
  unexpected behavior. This includes several key practices:


  **1. Handle Optional types correctly:** When working with Union types containing
  None, extract the non-None type before type checking to avoid `issubclass()` errors
  with type annotations.'
repository: stanfordnlp/dspy
label: Null Handling
language: Python
comments_count: 6
repository_stars: 27813
---

Implement proper null safety patterns to prevent runtime errors and unexpected behavior. This includes several key practices:

**1. Handle Optional types correctly:** When working with Union types containing None, extract the non-None type before type checking to avoid `issubclass()` errors with type annotations.

```python
def _strip_optional(ann):
    """If ann is Union[..., NoneType] return the non‑None part, else ann."""
    if get_origin(ann) is Union and NoneType in get_args(ann):
        return next(a for a in get_args(ann) if a is not NoneType)
    return ann
```

**2. Add dependency assertions for optional parameters:** When optional parameters have dependencies on each other, use assertions to validate the relationships.

```python
# Ensure dependent parameters are provided together
assert custom_instruction_proposer is None or reflection_lm is not None
# Or ensure at least one required parameter is provided  
assert custom_proposer is not None or reflection_lm is not None
```

**3. Avoid mutable default arguments:** Never use mutable objects as default parameter values, as they create shared state across function calls.

```python
# Wrong - shared mutable state
history: list[Completions] = Field(default=[])

# Correct - each instance gets its own list
history: list[Completions] = Field(default_factory=list)
```

**4. Use idiomatic null coalescing:** Prefer concise Python patterns for handling None values.

```python
# Prefer this concise pattern
self.interpreter = interpreter or PythonInterpreter()

# Over verbose None checks
self.interpreter = interpreter if interpreter is not None else PythonInterpreter()
```

**5. Avoid unnecessary Optional annotations:** Don't use Optional for parameters that have default values, as the default already handles the None case.

These patterns prevent common null-related bugs and make code more robust and maintainable.