---
title: Graceful API evolution
description: 'When evolving APIs, prioritize backward compatibility and provide clear
  migration paths. For any significant change:


  1. Add explicit deprecation warnings that explain what''s changing and how to adapt
  code'
repository: django/django
label: API
language: Python
comments_count: 5
repository_stars: 84182
---

When evolving APIs, prioritize backward compatibility and provide clear migration paths. For any significant change:

1. Add explicit deprecation warnings that explain what's changing and how to adapt code
2. Maintain backward compatibility during deprecation periods with shims or dual implementations
3. Document specific migration steps, ideally with before/after examples
4. Consider real-world usage patterns before removing or changing behavior

**Example of good practice:**

```python
# For changing from positional to keyword-only arguments:
@deprecate_posargs(RemovedInDjangoXXWarning, moved=["option1", "option2"])
def some_func(request, *, option1, option2=True):
    # Implementation
```

**Example of maintaining compatibility when changing property behavior:**

```python
@cached_property
def params(self):
    # Keep original behavior
    return self._params.copy()  # Still includes 'q' for backward compatibility

@cached_property  
def range_params(self):
    # New API with refined behavior
    params = self._params.copy()
    params.pop("q", None)  
    return params
```

Even for "non-public" APIs that have been available for extended periods, consider adding deprecation shims to prevent breaking dependent code in the ecosystem.