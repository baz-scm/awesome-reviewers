---
title: Extract repeated logic
description: When you notice code patterns being repeated across functions or methods,
  extract the common logic into separate, reusable functions. This improves maintainability,
  reduces bugs, and follows the DRY (Don't Repeat Yourself) principle.
repository: comfyanonymous/ComfyUI
label: Code Style
language: Python
comments_count: 9
repository_stars: 83726
---

When you notice code patterns being repeated across functions or methods, extract the common logic into separate, reusable functions. This improves maintainability, reduces bugs, and follows the DRY (Don't Repeat Yourself) principle.

Look for opportunities to:
- Extract repeated code blocks into helper functions
- Split complex functions that handle multiple responsibilities
- Create utility functions for common operations
- Refactor similar conditional logic into shared functions

Example of refactoring repeated logic:

```python
# Before: Repeated logic in multiple places
def get_free_memory(dev=None, torch_free_too=False):
    if os.path.isfile('/sys/fs/cgroup/memory/memory.limit_in_bytes'):
        with open('/sys/fs/cgroup/memory/memory.limit_in_bytes', 'r') as f:
            mem_used_total = psutil.virtual_memory().used
            mem_total = int(f.read())
            # ... more logic

def get_total_memory(dev=None):
    if os.path.isfile('/sys/fs/cgroup/memory/memory.limit_in_bytes'):
        with open('/sys/fs/cgroup/memory/memory.limit_in_bytes', 'r') as f:
            mem_used_total = psutil.virtual_memory().used
            mem_total = int(f.read())
            # ... more logic

# After: Extracted common logic
def get_containerd_memory_limit():
    if os.path.isfile('/sys/fs/cgroup/memory/memory.limit_in_bytes'):
        with open('/sys/fs/cgroup/memory/memory.limit_in_bytes', 'r') as f:
            mem_used_total = psutil.virtual_memory().used
            mem_total = int(f.read())
            return mem_used_total, mem_total
    return None, None

def get_free_memory(dev=None, torch_free_too=False):
    mem_used, mem_total = get_containerd_memory_limit()
    if mem_used is not None:
        # ... use extracted values
```

This approach makes code more maintainable, testable, and reduces the likelihood of introducing bugs when making changes.