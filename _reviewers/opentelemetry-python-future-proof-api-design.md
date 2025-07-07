---
title: Future-proof API design
description: Design APIs that can evolve without breaking existing code. Use keyword-only
  arguments (with `*,`) for optional parameters to make API extensions safer. This
  prevents positional argument errors when parameters change and allows for easier
  parameter reordering, addition, and deprecation.
repository: open-telemetry/opentelemetry-python
label: API
language: Python
comments_count: 7
repository_stars: 2061
---

Design APIs that can evolve without breaking existing code. Use keyword-only arguments (with `*,`) for optional parameters to make API extensions safer. This prevents positional argument errors when parameters change and allows for easier parameter reordering, addition, and deprecation.

```python
# Problematic: Adding parameters later can break existing callers
def create_counter(self, name: str, unit: str = "", description: str = ""):
    pass

# Better: Force keyword arguments for optional parameters
def create_counter(self, name: str, *, unit: str = "", description: str = "", 
                  advisory: Optional[MetricsCommonAdvisory] = None):
    pass
```

For types that may evolve structurally, use more generic container types or provide extension mechanisms. When designing class hierarchies, consider how derived classes will override methods - match parameter names and types carefully to avoid incompatibilities.

When introducing new functionality beyond the specification, implement it as utility functions rather than extending core interfaces. This prevents application code from becoming tightly coupled to specific implementations:

```python
# Avoid adding non-spec methods directly to SDK classes
class Histogram(_Synchronous, APIHistogram):
    def time(self):  # Problematic: Application code depends on SDK implementation
        return _Timer(self)

# Better: Create utility functions
def get_timer(histogram):  # Good: Application code uses utility function
    return _Timer(histogram)
```

This approach maintains clear boundaries between API contracts and implementation details while providing flexibility for future evolution.