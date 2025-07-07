---
title: Pythonic API design
description: Design APIs that follow Python language conventions and idioms rather
  than blindly mirroring the underlying implementation language. Consider what would
  feel most natural to Python developers in terms of parameter ordering, default values,
  and call patterns.
repository: huggingface/tokenizers
label: API
language: Python
comments_count: 3
repository_stars: 9868
---

Design APIs that follow Python language conventions and idioms rather than blindly mirroring the underlying implementation language. Consider what would feel most natural to Python developers in terms of parameter ordering, default values, and call patterns.

Key principles:
- Place frequently used parameters first, with optional parameters later using default values
- Use named arguments for optional parameters rather than positional ones
- Consider the readability and usability of parameter signatures from the Python developer's perspective
- Create convenient interfaces that hide complex internal data structures while preserving functionality

Example:
```python
# Instead of exposing complex implementation details:
def initialize(
    vocab: Optional[Union[str, Dict[str, int]]] = None,
    merges: Optional[Union[str, Dict[Tuple[int, int], Tuple[int, int]]]] = None,
)

# Provide a more Pythonic interface:
def initialize(
    files, 
    vocab_size=30000,
    min_frequency=2,
    special_tokens=None
)
```

When adapting APIs from other languages, prioritize what makes sense for Python users rather than strictly adhering to the source language patterns. This improves usability while reducing the learning curve for your library.