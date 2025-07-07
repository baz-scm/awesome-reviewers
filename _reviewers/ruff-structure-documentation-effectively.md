---
title: Structure documentation effectively
description: Documentation should follow a consistent structure where explanations
  precede code examples, preferably ending with a colon to introduce the code. When
  documenting special cases or complex behaviors, include links to relevant external
  specifications or standards. Consolidate similar documentation to avoid duplication
  across files.
repository: astral-sh/ruff
label: Documentation
language: Markdown
comments_count: 3
repository_stars: 40619
---

Documentation should follow a consistent structure where explanations precede code examples, preferably ending with a colon to introduce the code. When documenting special cases or complex behaviors, include links to relevant external specifications or standards. Consolidate similar documentation to avoid duplication across files.

Example:
```md
## The `nonlocal` keyword

Without the `nonlocal` keyword, `x += 1` (or `x = x + 1` or `x = foo(x)`) is not allowed in an inner
scope like this. It might look like it would read the outer `x` and write to the inner `x`, but it
actually tries to read the not-yet-initialized inner `x` and raises `UnboundLocalError` at runtime:

```py
def f():
    x = 1
    def g():
        x += 1  # error: [unresolved-reference]
```

See [Python language reference](https://docs.python.org/3/reference/simple_stmts.html#the-nonlocal-statement) for more details.
```