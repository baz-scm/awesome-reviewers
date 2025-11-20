---
title: comprehensive test assertions
description: Write robust test assertions that verify complete objects and behaviors
  rather than individual properties. Use pytest's built-in features for exception
  testing and mock verification to make tests more reliable and maintainable.
repository: strands-agents/sdk-python
label: Testing
language: Python
comments_count: 5
repository_stars: 4044
---

Write robust test assertions that verify complete objects and behaviors rather than individual properties. Use pytest's built-in features for exception testing and mock verification to make tests more reliable and maintainable.

Key practices:
- Use `pytest.raises(ExceptionType, match="expected message")` instead of manual exception handling
- Assert entire objects/messages rather than checking individual properties one by one
- Leverage mock verification methods like `call_args` instead of manual parameter capturing
- Verify actual behavior (like tool execution) through observable side effects

Example of improved assertions:
```python
# Instead of manual exception handling:
try:
    some_function()
    raise AssertionError("Expected an exception")
except ValueError as e:
    assert "expected message" in str(e)

# Use pytest.raises with match:
with pytest.raises(ValueError, match="expected message"):
    some_function()

# Instead of checking individual properties:
assert agent.messages[1]["role"] == "user"
assert "toolResult" in agent.messages[1]["content"][0]
assert agent.messages[1]["content"][0]["toolResult"]["toolUseId"] == "orphaned-123"

# Assert the complete structure:
expected_message = {
    "role": "user", 
    "content": [{"toolResult": {"toolUseId": "orphaned-123", ...}}]
}
assert agent.messages[1] == expected_message

# Instead of manual kwargs capturing:
def capture_kwargs(*args, **kwargs):
    capture_kwargs.captured_kwargs = kwargs

# Use mock verification:
assert mock_function.call_args == call(expected_args, **expected_kwargs)
```

This approach makes tests more readable, catches more potential issues, and reduces the likelihood of false positives in test results.