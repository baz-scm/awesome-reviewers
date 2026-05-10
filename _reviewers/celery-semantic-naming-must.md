---
title: Semantic Naming Must
description: 'Use naming conventions that are both tooling-correct and behavior-semantic:


  - **Tooling-sensitive identifiers:** If a subsystem matches by name (e.g., test
  discovery), ensure the identifier follows the project’s configured pattern—otherwise
  tests may be skipped silently.'
repository: celery/celery
label: Naming Conventions
language: Python
comments_count: 6
repository_stars: 28464
---

Use naming conventions that are both tooling-correct and behavior-semantic:

- **Tooling-sensitive identifiers:** If a subsystem matches by name (e.g., test discovery), ensure the identifier follows the project’s configured pattern—otherwise tests may be skipped silently.
- **Unambiguous semantics:** Names must distinguish different meanings/units/types (e.g., numeric timeout vs Timeout class). Avoid overloads like two similarly named “timeout” parameters.
- **Avoid misleading prefixes:** If a method named like `is_*` has side effects, it violates reader expectations. Either rename (e.g., `maybe_unlock`) or refactor to keep `is_*` side-effect-free.
- **Meaningful identifiers over abbreviations:** Prefer domain-relevant names over short variables that don’t explain themselves (e.g., `greenlet` over `gt`).
- **Accurate feature flag names:** Flags should describe the *actual* behavior they control, not a general concept.

Example patterns to follow:
```python
# Tooling-sensitive: matches `python_classes = "test_*"`
class test_pool_acquire_timeout:
    ...

# Semantic clarity: numeric timeout vs class
def apply_target(..., timeout=None, TimeoutClass=None, ...):
    ...

# Misleading name fix: keep `is_*` side-effect free
def is_locked(self):
    return os.path.exists(self.path)

def maybe_unlock(self):
    if self._is_stale():
        self.remove_if_stale()
```

If you’re unsure, pick the name that answers “what is it?” and “what does it do?” without consulting the implementation.