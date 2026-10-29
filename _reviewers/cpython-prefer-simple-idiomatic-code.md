---
title: Prefer simple, idiomatic code
description: 'Favor the simplest, most idiomatic construct that accomplishes the task,
  and remove any code that doesn''t add value. Concretely:


  - Use guard clauses to return early instead of nesting the rest of a function inside
  an `if`, which reduces indentation and improves readability:'
repository: python/cpython
label: Code Style
language: Python
comments_count: 7
repository_stars: 77696
---

Favor the simplest, most idiomatic construct that accomplishes the task, and remove any code that doesn't add value. Concretely:

- Use guard clauses to return early instead of nesting the rest of a function inside an `if`, which reduces indentation and improves readability:
  ```python
  # instead of
  def sigint_handler(self, signum, frame):
      if not self.nosigint:
          ...  # rest of the body nested here

  # prefer
  def sigint_handler(self, signum, frame):
      if self.nosigint:
          return
      ...
  ```
- Prefer existing standard-library helpers over manual boilerplate, e.g. use `pathlib.Path` for filesystem setup instead of chaining `os.path.join`/`os.mkdir`/`open(...).write(...)`, and use `functools.partial` instead of repeating near-identical lambdas.
- Drop redundant wrappers and comparisons that don't change behavior, such as wrapping an already-boolean expression in `bool(...)`, or using `is` where `==` is intended for value comparison.
- Avoid introducing an extra helper method/class when a one-line expression (e.g. `sum(1 for ... )`) is just as clear; only factor out code when it genuinely improves clarity or is reused.

Applying these checks during review keeps the codebase concise, reduces cognitive load, and prevents small stylistic inconsistencies from accumulating.