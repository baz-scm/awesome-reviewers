---
title: avoid local imports
description: Place all import statements at the top of the file as global imports
  rather than importing modules within functions or methods. Local imports reduce
  code readability, complicate dependency tracking, and can indicate poor code organization.
repository: oraios/serena
label: Code Style
language: Python
comments_count: 6
repository_stars: 14465
---

Place all import statements at the top of the file as global imports rather than importing modules within functions or methods. Local imports reduce code readability, complicate dependency tracking, and can indicate poor code organization.

**Why this matters:**
- Improves code readability by making dependencies explicit upfront
- Enables better static analysis and type checking
- Prevents import-related performance overhead in frequently called functions
- Makes dependency management and refactoring easier
- Follows Python PEP 8 style guidelines

**How to fix:**
Move all imports to the top of the file, organized in the standard order: standard library, third-party packages, then local modules.

**Example:**
```python
# Bad - local imports
def _setup_runtime_dependencies(cls, logger, config, settings):
    import os  # Should be at top
    import platform  # Should be at top
    
    if platform.system() == "Windows":
        # ...

# Good - global imports  
import os
import platform

def _setup_runtime_dependencies(cls, logger, config, settings):
    if platform.system() == "Windows":
        # ...
```

**Exceptions:**
Local imports are acceptable only in rare cases like:
- Avoiding circular import issues
- Optional dependencies that may not be available
- Heavy modules that are rarely used

In such cases, add a comment explaining why the local import is necessary.