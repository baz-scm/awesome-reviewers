---
title: Test isolation and assertions
description: When code under test uses shared mutable state (module globals, singletons,
  tool registrations) or introduces new public behaviors, unit tests must (1) assert
  meaningful outcomes/calls and (2) isolate themselves by resetting/restoring that
  shared state.
repository: awslabs/mcp
label: Testing
language: Python
comments_count: 5
repository_stars: 9545
---

When code under test uses shared mutable state (module globals, singletons, tool registrations) or introduces new public behaviors, unit tests must (1) assert meaningful outcomes/calls and (2) isolate themselves by resetting/restoring that shared state.

Practical rules:
- Never ship tests that “assert nothing”; at minimum assert returned values and/or that critical mocks were called with expected args.
- If the implementation mutates module-level objects (e.g., app/server/tool descriptions) or uses singletons (e.g., cached HTTP sessions), use an `autouse` fixture to snapshot/restore state before/after each test (or ensure the production code is idempotent).
- For new public APIs/helpers (factory hooks, region overrides, etc.), add direct unit tests for each new function/branch; don’t rely on incidental behavior in higher-level integration tests.
- Avoid brittle assertions against hardcoded literals (e.g., versions/config strings). Prefer stable sources (like `__version__`) or computed expectations.

Example pattern for isolation:
```python
import pytest

# Suppose module has a singleton/global that tests mutate/consume
import my_module

@pytest.fixture(autouse=True)
def isolate_module_state():
    snapshot = dict(my_module.SINGLETON.__dict__)  # or snapshot the singleton object reference
    yield
    my_module.SINGLETON.__dict__.update(snapshot)
    # or my_module.reset_singleton()
```

Example pattern for meaningful assertions:
```python
async def test_startup_calls_connection_factory(mocker, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["prog", "--region", "us-east-1", "--db_endpoint", "host"])
    internal = mocker.patch.object(server, "internal_create_connection", return_value=(object(), {"status": "Connected"}))
    mcp_run = mocker.patch.object(server.mcp, "run")
    server.main()

    internal.assert_called_once()  # not optional
    assert mcp_run.called
```

Applying these standards prevents flaky/cross-test failures, makes regressions detectable, and ensures new behavior is actually covered.