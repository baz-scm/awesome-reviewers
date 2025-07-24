---
title: avoid external test dependencies
description: Tests should not depend on external resources like real URLs, remote
  servers, or external APIs as these dependencies make tests flaky and unreliable.
  Instead, use local mock servers, stub responses, or dependency injection to simulate
  external behavior.
repository: docker/compose
label: Testing
language: Python
comments_count: 2
repository_stars: 35858
---

Tests should not depend on external resources like real URLs, remote servers, or external APIs as these dependencies make tests flaky and unreliable. Instead, use local mock servers, stub responses, or dependency injection to simulate external behavior.

When tests require external resources, create local alternatives that provide the same interface. For example, instead of making HTTP requests to real URLs, spin up a local static file server or use mocked HTTP responses.

Example of problematic approach:
```python
def test_down_url(self):
    url = 'https://raw.githubusercontent.com/docker/compose/...'
    # This creates a flaky test dependent on network and external service
```

Better approach:
```python
def test_down_url(self, mock_server):
    # Use a local mock server that serves the same content
    url = f'http://localhost:{mock_server.port}/docker-compose.yml'
```

This principle also applies to mocking internal dependencies - when code paths change and new components are exercised, ensure proper mocks are in place rather than relying on early exits or bypassing the actual execution flow.