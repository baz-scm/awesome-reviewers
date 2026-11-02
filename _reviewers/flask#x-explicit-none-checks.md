---
title: Explicit None checks
description: 'Always distinguish "no value" (`None`) from other falsy values like
  `0`, `""`, or `False`. Use `is None` / `is not None` for identity checks instead
  of truthy/falsy tests (`if x` or `== None`), since the latter can silently misbehave
  when a legitimate falsy value (e.g. port `0`, an empty blueprint, etc.) is passed
  in. For example, prefer:'
repository: pallets/flask#x
label: Null Handling
language: Python
comments_count: 5
repository_stars: 75163
---

Always distinguish "no value" (`None`) from other falsy values like `0`, `""`, or `False`. Use `is None` / `is not None` for identity checks instead of truthy/falsy tests (`if x` or `== None`), since the latter can silently misbehave when a legitimate falsy value (e.g. port `0`, an empty blueprint, etc.) is passed in. For example, prefer:

```python
# Wrong: treats 0 as "no value"
port = int(port or sn_port or default_port)

# Right: only falls back when the value is actually None
port = int(next(p for p in (port, sn_port, default_port) if p is not None))
```

Likewise, keep existing `is not None` checks when refactoring code for style — do not simplify `if x is not None:` to `if x:` purely for brevity, as this changes behavior and can hide bugs.

When a variable may remain unset depending on a conditional/exception path, explicitly initialize it to `None` (or an appropriate default) before the branching logic, rather than relying on it being defined only inside a branch. For example, when capturing an exception for later use outside the handler, set `error = None` beforehand (or use an `else` clause) so the variable is never undefined, avoiding `UnboundLocalError`:

```python
error = None
try:
    ...
except BuildError as e:
    error = e
```

Applying explicit `is None` checks and guaranteed initialization prevents subtle bugs around falsy-but-valid values and undefined variables, and makes intent clear to readers.</description>
