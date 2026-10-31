---
title: Use idiomatic pytest features
description: 'Favor pytest''s built-in testing utilities over manual, imperative patterns
  to keep tests concise, correct, and maintainable.


  - Exception testing: use `pytest.raises(ExceptionType)` as a context manager instead
  of manual try/except blocks with `assert False` in the except clause. Code after
  the line that raises inside the `with` block is unreachable and...'
repository: pallets/flask
label: Testing
language: Python
comments_count: 9
repository_stars: 75022
---

Favor pytest's built-in testing utilities over manual, imperative patterns to keep tests concise, correct, and maintainable.

- Exception testing: use `pytest.raises(ExceptionType)` as a context manager instead of manual try/except blocks with `assert False` in the except clause. Code after the line that raises inside the `with` block is unreachable and should be removed.

```python
# Avoid
try:
    flask.send_from_directory('static', 'bad\x00')
    assert False
except BadRequest:
    pass

# Prefer
with pytest.raises(BadRequest):
    flask.send_from_directory('static', 'bad\x00')
```

- Repetitive cases: use `@pytest.mark.parametrize` instead of manually looping over inputs or duplicating near-identical test functions. Split combined fixture data into separate parameters (e.g. `("args", "expected")`) rather than bundling them into a single tuple/list fixture.

- Optional dependencies: guard tests that require optional packages with `pytest.importorskip('package_name')` so the suite can still run without them.

- Grouping related skips: when multiple tests share the same skip condition (e.g. requiring `greenlet`), group them into a test class and apply `pytest.mark.skipif` once at the class level instead of repeating it per test.

- Fixtures/signals: prefer pytest's `yield_fixture` (or a fixture using `yield`) for setup/teardown logic, and use context managers provided by libraries (e.g. blinker's `signal.connected_to`) for temporary connections, instead of manual connect/disconnect or ad-hoc fixture plumbing.

Applying these patterns reduces boilerplate, avoids subtle bugs (such as code after a raising call never executing), and makes test intent and coverage easier to follow.