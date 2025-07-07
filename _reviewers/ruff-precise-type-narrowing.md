---
title: Precise type narrowing
description: 'Implement sound type narrowing algorithms that balance precision with
  correctness. When narrowing types:


  1. For direct assignments, narrow the type to the assigned value''s type:'
repository: astral-sh/ruff
label: Algorithms
language: Markdown
comments_count: 8
repository_stars: 40619
---

Implement sound type narrowing algorithms that balance precision with correctness. When narrowing types:

1. For direct assignments, narrow the type to the assigned value's type:
```python
x: int | None = None
x = 42
# x now has type Literal[42]
```

2. For attributes and subscripts, only narrow when the operation is known to be sound:
- Narrow attribute assignments except for properties and descriptors
- Only narrow subscripts for built-in types with well-defined behavior (`list`, `dict`, etc.)
```python
# Sound - regular attribute
obj.attr = "value"  # obj.attr now has type Literal["value"]

# Unsound - property may transform the value
@property
def x(self): return self._x
@x.setter
def x(self, val): self._x = abs(val)
obj.x = -1  # obj.x should still be int, not Literal[-1]
```

3. Reset narrowed types when the base object is reassigned:
```python
c = C()
c.attr = "foo"  # c.attr has type Literal["foo"]
c = C()         # c.attr should revert to its declared type
```

4. For type guards, correctly intersect the original type with the guarded type:
```python
def is_int(x: object) -> TypeIs[int]: ...

def func(x: Any):
    if is_int(x):
        # x has type Any & int
```

Sound type narrowing algorithms prevent false negatives while maintaining precision, allowing for safer and more robust code.