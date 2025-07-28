---
title: Document complex code
description: Add explanatory comments or docstrings for complex, specialized, or non-obvious
  code that may not be immediately clear to other developers. This includes magic
  constants, platform-specific operations, advanced APIs, and implementation decisions
  with specific reasoning.
repository: comfyanonymous/ComfyUI
label: Documentation
language: Python
comments_count: 4
repository_stars: 83726
---

Add explanatory comments or docstrings for complex, specialized, or non-obvious code that may not be immediately clear to other developers. This includes magic constants, platform-specific operations, advanced APIs, and implementation decisions with specific reasoning.

Key areas requiring documentation:
- Magic numbers or constants with their meaning and purpose
- Platform-specific or specialized API usage (like win32 operations)
- Functions using advanced or uncommon techniques
- Implementation choices with specific technical reasoning
- File-level docstrings for modules dealing with specialized domains

Example for magic constants:
```python
# Windows Low Integrity Level SID - restricts process permissions for sandboxing
LOW_INTEGRITY_SID_STRING = "S-1-16-4096"
```

Example for specialized functions:
```python
def set_process_integrity_level_to_low():
    """
    Set the current process to run at a low integrity level.
    
    This restricts the process's permissions, creating a sandboxed environment
    to limit potential damage if compromised.
    """
```

Example for implementation decisions:
```python
# Use .tmp suffix during download to prevent incomplete state if interrupted
# Otherwise CTRL+C during download leaves ComfyUI thinking frontend is installed
tmp_path = web_root + ".tmp"
```

This ensures code maintainability and helps other developers understand the reasoning behind complex or specialized implementations.