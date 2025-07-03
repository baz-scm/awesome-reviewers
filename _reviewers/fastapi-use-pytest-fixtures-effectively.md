---
title: Use pytest fixtures effectively
description: Tests should use pytest fixtures to improve organization, promote test
  isolation, and avoid code duplication. Fixtures provide a clean way to set up test
  dependencies, manage test state, and create reusable test components.
repository: fastapi/fastapi
label: Testing
language: Python
comments_count: 4
repository_stars: 86871
---

Tests should use pytest fixtures to improve organization, promote test isolation, and avoid code duplication. Fixtures provide a clean way to set up test dependencies, manage test state, and create reusable test components.

Key principles:
- Use fixtures for test setup instead of global variables to prevent test pollution
- Monkeypatch environment variables and dependencies within fixtures
- Extract repetitive test code into parameterized fixtures
- Use session or module-level fixtures for expensive setup operations
- Store test constants in fixtures or dedicated constant files

Example:
```python
# Before: Using global variables and repetitive code
counter_holder = {"counter": 0, "parsing_counter": 0}  # Risky global state

def get_client_with_custom_config(config_value):
    app = FastAPI(config=config_value)
    return TestClient(app)

def test_feature_a():
    client = get_client_with_custom_config("value1")
    # Test implementation...

def test_feature_b():
    client = get_client_with_custom_config("value2")
    # Test implementation...

# After: Using pytest fixtures
@pytest.fixture
def counter():
    return {"counter": 0, "parsing_counter": 0}  # Isolated for each test

@pytest.fixture
def client(request):
    config_value = request.param
    app = FastAPI(config=config_value)
    return TestClient(app)

@pytest.mark.parametrize("client", ["value1", "value2"], indirect=True)
def test_features(client, counter):
    # Test implementation using client and counter...
```

Using fixtures properly improves test isolation, prevents unexpected side effects between tests, and makes test maintenance easier by centralizing common setup logic.