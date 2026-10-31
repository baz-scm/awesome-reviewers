---
title: Idiomatic, minimal Python constructs
description: 'Favor clear, idiomatic Python over verbose, manual, or unpythonic constructs,
  and avoid introducing unnecessary complexity or unrelated refactors just to satisfy
  a linter/type-checker. Specifically:'
repository: pallets/flask
label: Code Style
language: Python
comments_count: 11
repository_stars: 75022
---

Favor clear, idiomatic Python over verbose, manual, or unpythonic constructs, and avoid introducing unnecessary complexity or unrelated refactors just to satisfy a linter/type-checker. Specifically:

- Replace manual loops with comprehensions or built-ins when possible. E.g. use `[(category, x) for x in values]` instead of `map(lambda x: (category, x), values)`, use `dict.update(other)` instead of a manual union loop, use `for i, x in enumerate(items)` instead of manual indexing, and prefer `for...else` over manual "found" flags.
- Collapse trivial conditionals into direct expressions: `return all(...)` instead of `if all(...): return True`, or `provide_automatic_options = "OPTIONS" not in methods` instead of a multi-branch if/else that only sets a boolean.
- Use the correct idiom for type/identity checks: `callable(obj)` instead of `hasattr(obj, '__call__')`, `isinstance(x, str)` instead of `type(x) is str`, and `==` (never `is`) for comparing values like numbers or strings.
- Don't add redundant code that has no effect, such as a `t.cast()` that doesn't change the inferred type, an unnecessary `import` of a module already imported at module scope, or explicitly passing a default value (e.g. `None`) that's already the implicit default.
- When fixing an unrelated issue (e.g. a type-checker complaint), prefer the smallest possible change (e.g. a `# type: ignore` comment) over refactoring working code, especially in hot paths where extra variables/calls aren't free.
- Keep ordering-sensitive logic in ordered structures (lists/tuples), not sets, since set iteration order isn't guaranteed.

Example:
```python
# Avoid
results = []
for category, values in flashes.items():
    results += map(lambda x: (category, x), values)

# Prefer
results = [(category, x) for category, values in flashes.items() for x in values]
```

Applying this standard keeps diffs small, logic easy to scan, and avoids subtle bugs introduced by overly clever or needlessly verbose code.