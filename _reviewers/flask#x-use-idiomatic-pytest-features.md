---
title: Use idiomatic pytest features
description: 'Favor built-in pytest mechanisms over manual boilerplate to keep tests
  concise, correct, and properly isolated.


  - Use `pytest.raises(ExceptionType)` instead of manual `try/except` blocks to assert
  that an exception is raised; don''t add code after the raising call that can never
  execute.'
repository: pallets/flask#x
label: Testing
language: Python
comments_count: 13
repository_stars: 75163
---

Favor built-in pytest mechanisms over manual boilerplate to keep tests concise, correct, and properly isolated.

- Use `pytest.raises(ExceptionType)` instead of manual `try/except` blocks to assert that an exception is raised; don't add code after the raising call that can never execute.
- Use shared fixtures (e.g. `app`, `client`, `app_ctx`) instead of re-creating a `Flask` app/context by hand in every test; be mindful of fixture scope so each test still gets the isolation it needs (e.g. separate app contexts when previously each test created its own).
- Use `monkeypatch` (or `yield`-based fixtures) for patching globals/env vars instead of mutating module attributes directly; always restore/clean up state, even if a later assertion fails, by doing the teardown after a `yield` in the fixture rather than returning a value.
- Use `pytest.importorskip` to skip tests cleanly when an optional dependency isn't installed, rather than failing the whole suite.
- Use `pytest.mark.parametrize` to replace repetitive near-duplicate test functions/assertions with a single parametrized test; when parametrizing multiple related values, pass them as separate parameters (e.g. `"args, expected"`) rather than bundling them into one tuple parameter.
- When a test touches external resources (temp files, signals, sockets), ensure proper cleanup: close/remove temp files (prefer `tmp_path`/`NamedTemporaryFile` with a `with` block over manual `mkstemp`), and use available context managers (e.g. `Signal.connected_to`) to connect/disconnect signals instead of manual try/finally.
- Don't rely on non-deterministic ordering (e.g. iterating a `set`) in assertions; sort or otherwise normalize the data before comparing.

Example, converting a manual exception check to the idiomatic form:

```python
# Before
try:
    flask.send_from_directory('static', 'bad\x00')
    assert False
except BadRequest:
    pass

# After
with pytest.raises(BadRequest):
    flask.send_from_directory('static', 'bad\x00')
```

Applying these patterns reduces boilerplate, avoids subtle bugs (e.g. leftover patched state, unclosed files, assertions that can never run), and makes test intent clearer.