---
title: Behavior-First Pytest Testing
description: 'Write tests that are pytest-native, high-signal, and behavior-focused.


  Apply these rules:

  - Prefer observable behavior over internal plumbing: assert what the client uses
  during the request lifecycle (e.g., what headers are present when a request is made
  or when `auth_headers` is accessed), not just that a helper method mutates a field.'
repository: openai/openai-python
label: Testing
language: Python
comments_count: 6
repository_stars: 30731
---

Write tests that are pytest-native, high-signal, and behavior-focused.

Apply these rules:
- Prefer observable behavior over internal plumbing: assert what the client uses during the request lifecycle (e.g., what headers are present when a request is made or when `auth_headers` is accessed), not just that a helper method mutates a field.
- Reduce duplication with parametrization for equivalent endpoint/client variations.
- Avoid redundant test frameworks: don’t keep a `unittest.TestCase` version if a pytest equivalent already exists.
- Use inline snapshots for stable, structured outputs (schemas/JSON) instead of many repetitive manual assertions.
- Keep async markers minimal/consistent: only add `@pytest.mark.asyncio` if your environment/setup requires it.
- Add targeted regression coverage for subtle runtime behaviors (e.g., lazy module resolution and identity after reload).

Example (high-signal header behavior):
```python
def test_auth_headers_set_before_request() -> None:
    client = OpenAI(base_url=base_url, api_key=lambda: "test_bearer_token")
    # Access/trigger the behavior you actually rely on at request time
    client.auth_headers  # should force/ensure correct Authorization value
    assert client.auth_headers["Authorization"] == "Bearer test_bearer_token"
```

Example (parametrize endpoints):
```python
@pytest.mark.parametrize("path", ["/images/generations", "/chat/completions"])
def test_model_stripped_from_body(client: Client, path: str) -> None:
    req = client._build_request(
        FinalRequestOptions.construct(method="post", url=path, json_data={"model": "gpt-image-1-5", "prompt": "sunset"})
    )
    assert "model" not in req.json
```

Example (inline snapshot idea):
```python
def test_schema_snapshot() -> None:
    schema = to_strict_json_schema(MyModel)
    assert schema == {"type": "object", "additionalProperties": False, "properties": {...}, "required": [...]}
    # or use an inline snapshot if your codebase supports it
```

Example (lazy import regression assertion):
```python
import importlib
import openai
m1 = openai.types
m2 = importlib.reload(openai.types)
assert m1 is m2
```