---
title: Mock tests in tests/litellm
description: All new functionality must include mock tests placed in the `tests/litellm/`
  directory structure. Mock external API calls and dependencies rather than requiring
  real credentials or external services. This ensures tests can run reliably in CI/CD
  pipelines and are accessible to all contributors.
repository: BerriAI/litellm
label: Testing
language: Python
comments_count: 12
repository_stars: 28310
---

All new functionality must include mock tests placed in the `tests/litellm/` directory structure. Mock external API calls and dependencies rather than requiring real credentials or external services. This ensures tests can run reliably in CI/CD pipelines and are accessible to all contributors.

**Key Requirements:**
- Place tests in `tests/litellm/` following the source code structure (e.g., `tests/litellm/llms/provider_name/`)
- Mock external API calls using `unittest.mock` or `pytest-mock` instead of making real API requests
- Avoid tests that require external credentials, API keys, or network dependencies
- Use `MagicMock` to simulate responses from external services

**Example:**
```python
# Good: Mock test in tests/litellm/
from unittest.mock import patch, MagicMock
import pytest
from litellm import completion

def test_provider_completion_mock():
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "choices": [{"message": {"content": "Hello"}}]
    }
    
    with patch("requests.post", return_value=mock_response):
        response = completion(
            model="provider/model-name",
            messages=[{"role": "user", "content": "Hi"}]
        )
        assert response.choices[0].message.content == "Hello"

# Bad: Integration test requiring real credentials
def test_provider_completion_real():
    # Requires PROVIDER_API_KEY environment variable
    response = completion(
        model="provider/model-name", 
        messages=[{"role": "user", "content": "Hi"}]
    )
```

This approach prevents test failures due to missing credentials, network issues, or rate limits, while ensuring comprehensive test coverage that contributors can run locally and in automated pipelines.