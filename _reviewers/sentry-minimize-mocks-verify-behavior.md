---
title: Minimize mocks verify behavior
description: Write tests that verify actual system behavior rather than implementation
  details by minimizing mock usage and focusing on real interactions. Excessive mocking
  can lead to brittle tests that pass even when core functionality is broken.
repository: getsentry/sentry
label: Testing
language: Python
comments_count: 7
repository_stars: 41297
---

Write tests that verify actual system behavior rather than implementation details by minimizing mock usage and focusing on real interactions. Excessive mocking can lead to brittle tests that pass even when core functionality is broken.

Key guidelines:
1. Prefer real implementations over mocks when practical
2. When mocking is necessary, mock at system boundaries rather than internal components
3. Use built-in test helpers (e.g. @override_options) instead of mocking configuration
4. Break complex test scenarios into separate focused test methods

Example - Instead of:
```python
@patch("sentry.api.endpoints.seer_rpc.integration_service.get_organization_integrations")
@patch("sentry.api.endpoints.seer_rpc.options.get")
def test_complex_scenario(self, mock_options, mock_integrations):
    mock_integrations.return_value = []
    mock_options.return_value = []
    # Test implementation
```

Prefer:
```python
@override_options({"feature.flag": True})
def test_complex_scenario(self):
    # Create real integration
    integration = self.create_integration(
        organization=self.organization,
        provider="github"
    )
    # Test actual behavior
```

This approach produces more reliable tests that better verify system correctness and are easier to maintain.