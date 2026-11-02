---
title: Idiomatic, simplified Python style
description: 'Write code that is idiomatic, simplified, and consistent with the rest
  of the codebase rather than clever or verbose. Concretely:


  - Prefer built-in functions and idioms over manual reimplementations: use `callable(obj)`
  instead of `hasattr(obj, ''__call__'')`, `isinstance(obj, str)` instead of `type(obj)
  is str`, `repr(obj)` instead of calling...'
repository: pallets/flask#x
label: Code Style
language: Python
comments_count: 15
repository_stars: 75163
---

Write code that is idiomatic, simplified, and consistent with the rest of the codebase rather than clever or verbose. Concretely:

- Prefer built-in functions and idioms over manual reimplementations: use `callable(obj)` instead of `hasattr(obj, '__call__')`, `isinstance(obj, str)` instead of `type(obj) is str`, `repr(obj)` instead of calling `obj.__repr__()`, and `os.path.join(...)` instead of manual string concatenation for paths.
- Avoid unpythonic constructs such as `map()` with a `lambda`; use a list/dict comprehension instead, e.g. prefer `[(category, x) for x in values]` over `map(lambda x: (category, x), values)`.
- Simplify boolean logic: return the expression directly instead of wrapping it in `if/else` (`return all(...)` rather than `if all(...): return True else: return False`), and avoid redundant comparisons like `assert x == True` or `assert x == False`—use `assert x` or `assert not x` instead.
- Don't overcomplicate simple assignments with ternaries or conditional chains, e.g. use `provide_automatic_options = "OPTIONS" not in methods` rather than a verbose `if/else` or convoluted ternary when the logic is a single boolean expression.
- Use plain comments (`#`) rather than docstrings for inline/implementation notes; reserve docstrings for documenting the public interface.
- Avoid unnecessary escaping in string literals (prefer `"<flask.g of 'flask_test'>"` over an escaped-quote variant) and remove needless classes/instances when module-level functions or constants suffice.
- Maintain consistent formatting: use spaces (never tabs) for indentation, keep a blank line before new code blocks, and stick to the string-formatting style already used throughout the file/module (e.g. don't mix `%`-formatting and `.format()` within the same area unless there's a dedicated migration PR).

Following these guidelines keeps the codebase readable, consistent, and free of unnecessary complexity introduced by non-idiomatic or verbose constructs.