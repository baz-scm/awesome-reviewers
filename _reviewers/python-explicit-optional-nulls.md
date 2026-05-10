---
title: Explicit Optional Nulls
description: 'When a value can be absent, represent that absence explicitly and consistently.


  **Do**

  - Use `Optional[...]`/`T | None` in type hints for nullable inputs, outputs, and
  pointers.'
repository: TheAlgorithms/Python
label: Null Handling
language: Python
comments_count: 6
repository_stars: 220912
---

When a value can be absent, represent that absence explicitly and consistently.

**Do**
- Use `Optional[...]`/`T | None` in type hints for nullable inputs, outputs, and pointers.
- Initialize missing references (e.g., children, root) to `None`—never to a placeholder like `self`.
- For empty inputs, set the owning state to `None` (or return early) rather than creating dummy nodes that look valid.
- Keep function return contracts consistent: if an API can’t produce a result, return `None` (or use a single sentinel), and type it accordingly.
- If `None` is only used to mean “use default behavior,” prefer a non-`None` default argument.

**Example (segment-tree style):**
```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class Node:
    start: int
    end: int
    value: int = 0
    left: Optional["Node"] = None
    right: Optional["Node"] = None

class SegmentTree:
    def __init__(self, nums: list[int]) -> None:
        self.root: Optional[Node] = None
        if not nums:
            return
        self.root = self.build(0, len(nums) - 1, nums)
```

Applying this standard prevents null-reference bugs, removes confusing placeholder behavior, and makes absence handling readable and enforceable by both humans and type checkers.