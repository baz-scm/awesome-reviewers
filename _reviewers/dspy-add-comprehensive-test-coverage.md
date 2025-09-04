---
title: Add comprehensive test coverage
description: When introducing new functionality, always include corresponding test
  coverage that extends existing test infrastructure and validates the feature across
  multiple scenarios. This ensures robustness and maintains code quality standards.
repository: stanfordnlp/dspy
label: Testing
language: Markdown
comments_count: 2
repository_stars: 27813
---

When introducing new functionality, always include corresponding test coverage that extends existing test infrastructure and validates the feature across multiple scenarios. This ensures robustness and maintains code quality standards.

Key practices:
- Extend existing test utilities and infrastructure rather than creating isolated tests
- Write integration tests that validate end-to-end functionality
- Test across different configurations and edge cases
- Follow established testing patterns in the codebase

Example approach:
```python
# When adding streaming functionality, extend existing test server
# tests/test_utils/server/litellm_server.py - add streaming endpoint

# Create integration test in appropriate location
# tests/streaming.py
def test_streaming_endpoint():
    # Use existing test infrastructure like litellm_test_server
    # Test the complete flow: configure -> run program -> validate stream
    stream = streaming_dspy_program(question=question.text)
    # Validate streaming response format and content
```

This approach ensures that new features are thoroughly validated and integrate seamlessly with existing systems, reducing the likelihood of regressions and improving overall system reliability.