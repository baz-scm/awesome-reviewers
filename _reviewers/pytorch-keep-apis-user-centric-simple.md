---
title: Keep APIs user-centric simple
description: Design APIs with a focus on simplicity and user experience, especially
  for first-time users. Complex functionality should be encapsulated in well-structured
  protocols or classes rather than exposed through numerous optional parameters.
repository: pytorch/pytorch
label: API
language: Python
comments_count: 4
repository_stars: 91169
---

Design APIs with a focus on simplicity and user experience, especially for first-time users. Complex functionality should be encapsulated in well-structured protocols or classes rather than exposed through numerous optional parameters.

Key principles:
1. Avoid loose, contextless function calls (e.g. global `close()`)
2. Encapsulate related parameters in protocol/class properties
3. Keep basic usage simple while allowing advanced configurations
4. Place complex functionality behind clear abstractions

Example - Instead of:
```python
def async_save(
    state_dict,
    storage_writer,
    async_stager=None,
    block_on_staging=True,
    process_group=None,
    async_checkpointer_type=AsyncCheckpointerType.THREAD,
):
    # Complex implementation
```

Better approach:
```python
class AsyncStager:
    def __init__(self, config: AsyncStagerConfig):
        self.block_on_staging = config.block_on_staging
        self.checkpointer_type = config.checkpointer_type
        
    def async_save(self, state_dict, storage_writer):
        # Implementation with config properties
```

This makes the basic API simple while allowing advanced users to configure behavior through well-defined configuration objects.
