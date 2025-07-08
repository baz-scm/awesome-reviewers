---
title: Parameterize similar tests
description: Write maintainable tests by using pytest parametrization for similar
  test cases instead of duplicating test logic. This makes tests easier to read, maintain,
  and extend when requirements change.
repository: prowler-cloud/prowler
label: Testing
language: Python
comments_count: 3
repository_stars: 11834
---

Write maintainable tests by using pytest parametrization for similar test cases instead of duplicating test logic. This makes tests easier to read, maintain, and extend when requirements change.

For example, instead of writing multiple similar test functions:

```python
# Before: Repetitive test functions
def test_invalid_name(self, client, payload):
    payload["data"]["attributes"]["name"] = "T"  # Too short
    response = client.post("/endpoint/", data=payload)
    assert response.status_code == 400
    assert "name" in response.json()["errors"][0]["source"]["pointer"]

def test_invalid_api_key(self, client, payload):
    payload["data"]["attributes"]["api_key"] = "invalid"  # Invalid format
    response = client.post("/endpoint/", data=payload)
    assert response.status_code == 400
    assert "api_key" in response.json()["errors"][0]["source"]["pointer"]
```

Use pytest parametrization to consolidate test logic:

```python
# After: Parametrized test
@pytest.mark.parametrize(
    "field,value,expected_error",
    [
        ("name", "T", "name"),  # Too short
        ("api_key", "invalid", "api_key"),  # Invalid format
        ("temperature", 2.0, "temperature"),  # Out of range
        ("max_tokens", -1, "max_tokens"),  # Invalid value
    ],
)
def test_invalid_field_validation(self, client, valid_payload, field, value, expected_error):
    """Test validation failures for various invalid fields"""
    payload = copy.deepcopy(valid_payload)
    payload["data"]["attributes"][field] = value
    
    response = client.post("/endpoint/", data=payload, content_type=API_JSON_CONTENT_TYPE)
    assert response.status_code == 400
    errors = response.json()["errors"]
    assert any(expected_error in error["source"]["pointer"] for error in errors)
```

Also use fixtures to setup test data properly instead of relying on other tests:

```python
@pytest.fixture
def lighthouse_config_fixture(db):
    """Create a test configuration in the database"""
    return LighthouseConfig.objects.create(
        name="Test Config",
        api_key="sk-test1234567890T3BlbkFJtest1234567890",
        model="gpt-4o"
    )
```

This approach reduces code duplication, improves readability, and makes it easier to add test cases as requirements evolve.