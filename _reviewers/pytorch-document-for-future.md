---
title: Document for future
description: 'Write documentation that serves developers who will read your code months
  or years from now, not just yourself. When documenting complex logic, public APIs,
  or implementation details:'
repository: pytorch/pytorch
label: Documentation
language: Python
comments_count: 5
repository_stars: 91169
---

Write documentation that serves developers who will read your code months or years from now, not just yourself. When documenting complex logic, public APIs, or implementation details:

1. **Be thorough and clear** - Don't be frugal with words when explaining critical functionality or design decisions. Explain the "why" behind complex code, not just the "what."

2. **Provide complete context** - For public APIs and classes, include comprehensive docstrings that explain purpose, usage patterns, and edge cases.

3. **Explain different scenarios** - When logic handles multiple cases or has non-obvious behavior, document all scenarios.

Example of insufficient documentation:
```python
# NOTE: num_heads attributes are not mandatory for 4D.
```

Improved version:
```python
# NOTE: num_heads attributes (q_num_heads/kv_num_heads) should NOT be 
# specified for 4D inputs. While the ONNX specification allows these 
# attributes for all input formats, including them with 4D inputs will 
# cause inconsistent behavior across runtimes. Only specify these
# attributes when using 3D inputs ([B, S, N*H]).
```

Remember that comments which seem clear when you write them may be cryptic to someone revisiting the code later. Write documentation that will stand the test of time.
