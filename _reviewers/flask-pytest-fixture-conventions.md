---
title: Pytest fixture conventions
description: Standardize tests on pytest and follow its conventions for structure
  and fixtures. Place tests in a `tests/` directory without an `__init__.py` (pytest
  treats it as a plain directory, not a package), and name test files `test_*.py`
  so they are auto-discovered. For setup/teardown logic, prefer `yield` fixtures over
  `request.addfinalizer`, since they are more...
repository: pallets/flask
label: Testing
language: Other
comments_count: 3
repository_stars: 75022
---

Standardize tests on pytest and follow its conventions for structure and fixtures. Place tests in a `tests/` directory without an `__init__.py` (pytest treats it as a plain directory, not a package), and name test files `test_*.py` so they are auto-discovered. For setup/teardown logic, prefer `yield` fixtures over `request.addfinalizer`, since they are more concise and keep setup and teardown code together:

```python
import os
import tempfile
import pytest
from flaskr import flaskr

@pytest.fixture
def client():
    db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
    flaskr.app.config['TESTING'] = True
    client = flaskr.app.test_client()
    with flaskr.app.app_context():
        flaskr.init_db()

    yield client

    os.close(db_fd)
    os.unlink(flaskr.app.config['DATABASE'])
```

Additionally, configure the test runner (e.g. `tox.ini`) to run `py.test` with coverage reporting enabled (`--cov=<package> --cov-report html`) and keep the ability to pass through extra arguments (e.g. `py.test {posargs}`) so individual tests can be targeted from the command line.