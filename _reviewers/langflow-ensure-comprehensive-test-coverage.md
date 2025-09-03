---
title: Ensure comprehensive test coverage
description: Always add test coverage for new functionality, especially when introducing
  integrations or services. Use mocks and patches when testing external dependencies.
  Additionally, configure coverage reporting to exclude irrelevant paths like legacy
  components, deactivated features, and test files themselves to maintain meaningful
  coverage metrics.
repository: langflow-ai/langflow
label: Testing
language: Python
comments_count: 2
repository_stars: 111046
---

Always add test coverage for new functionality, especially when introducing integrations or services. Use mocks and patches when testing external dependencies. Additionally, configure coverage reporting to exclude irrelevant paths like legacy components, deactivated features, and test files themselves to maintain meaningful coverage metrics.

Example coverage configuration:
```python
# .coveragerc
[run]
source = src/backend/base/langflow
omit =
    # Test files
    */tests/*
    */test_*
    
    # Deactivated Components
    */components/deactivated/*
    
    # Legacy components with legacy = True
    */components/legacy_component.py
```

When adding tests, use appropriate mocking:
```python
# Example test with mocking
@patch('module.external_service')
def test_tracing_functionality(mock_service):
    mock_service.return_value = expected_result
    # Test implementation
    assert result == expected_result
```