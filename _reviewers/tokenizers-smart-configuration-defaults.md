---
title: Smart configuration defaults
description: Prefer smart configuration defaults that auto-detect the environment
  instead of requiring explicit configuration flags. When possible, implement automatic
  detection of the runtime context and provide sensible defaults while still allowing
  explicit overrides.
repository: huggingface/tokenizers
label: Configurations
language: Python
comments_count: 2
repository_stars: 9868
---

Prefer smart configuration defaults that auto-detect the environment instead of requiring explicit configuration flags. When possible, implement automatic detection of the runtime context and provide sensible defaults while still allowing explicit overrides.

For example, instead of requiring a boolean flag to control behavior:
```python
def __init__(
    self,
    tokenizer: Tokenizer,
    default_to_notebook: bool = False,
    # ...
)
```

Consider auto-detecting the environment:
```python
def __init__(
    self,
    tokenizer: Tokenizer,
    # No default_to_notebook parameter needed
    # ...
):
    # Auto-detect if running in a notebook environment
    use_notebook = _is_in_notebook_environment()
    # ...
```

Similarly, when changing configuration parameters for backward compatibility, translate legacy boolean parameters to more descriptive string options:
```python
# Instead of directly using boolean parameter
prepend_scheme = "always" if add_prefix_space else "never"
```

This approach reduces configuration burden on users, provides more intuitive defaults, and makes the API more user-friendly while maintaining compatibility with existing code.