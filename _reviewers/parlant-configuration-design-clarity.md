---
title: Configuration design clarity
description: Design configuration with clear semantics and appropriate scope. Avoid
  global constants for values that can be handled locally, and ensure configuration
  parameters have logical, non-contradictory meanings.
repository: emcie-co/parlant
label: Configurations
language: Other
comments_count: 2
repository_stars: 12205
---

Design configuration with clear semantics and appropriate scope. Avoid global constants for values that can be handled locally, and ensure configuration parameters have logical, non-contradictory meanings.

**Avoid unnecessary global configuration constants:**
```python
# Instead of:
DEFAULT_PORT = 8000
DEFAULT_INDEX = True  # Global constants

# Consider handling defaults in-context:
def setup_server(port=8000, enable_indexing=False):
    # Handle defaults locally where they're used
```

**Design clear configuration interfaces:**
```python
# Avoid contradictory parameters:
# Bad: Indexer(perform_indexing=True, force_disable_indexing=True)

# Better: Handle configuration logic at application level:
if params.index and not params.force_disable:
    indexer = Indexer(index_json_file=path)
    # Use indexer
else:
    # Skip indexing entirely
```

Configuration should be intuitive - parameters shouldn't require mental gymnastics to understand their combined effect. Keep configuration logic at the appropriate architectural level rather than pushing contradictory options down to individual components.