---
title: Use descriptive names
description: Choose descriptive, self-documenting names for constants, functions,
  parameters, and types that clearly communicate their purpose and meaning. Avoid
  magic numbers, generic strings, and ambiguous identifiers that require additional
  context to understand.
repository: comfyanonymous/ComfyUI
label: Naming Conventions
language: Python
comments_count: 6
repository_stars: 83726
---

Choose descriptive, self-documenting names for constants, functions, parameters, and types that clearly communicate their purpose and meaning. Avoid magic numbers, generic strings, and ambiguous identifiers that require additional context to understand.

Replace magic values with named constants:
```python
# Instead of:
win32event.WaitForSingleObject(hProcess, 10 * 1000)

# Use:
TEN_SECONDS_MS = 10 * 1000
win32event.WaitForSingleObject(hProcess, TEN_SECONDS_MS)
```

Use semantic constants instead of magic strings:
```python
# Instead of:
{"source": ("*", {})}

# Use:
{"source": (node_typing.IO.ANY, {})}
```

Choose accurate function names that reflect their actual behavior:
```python
# Instead of:
def init_builtin_custom_nodes():

# Use:
def init_builtin_extra_nodes():
```

Use specific type annotations that communicate intent:
```python
# Instead of:
def filter_files_content_types(files: List[str], content_types: List[str]) -> List[str]:

# Use:
def filter_files_content_types(files: List[str], content_types: Literal["image", "video", "audio"]) -> List[str]:
```

This practice makes code self-documenting, reduces the need for comments, and helps prevent misunderstandings about the code's purpose and behavior.