---
title: Test independence design
description: Tests should be designed to be independent and avoid coupling to implementation
  details. Use public interfaces rather than accessing internal state, prefer mocked
  or fake data over external dependencies, and keep tests general rather than tightly
  coupled to specific implementations.
repository: commaai/openpilot
label: Testing
language: Python
comments_count: 3
repository_stars: 58214
---

Tests should be designed to be independent and avoid coupling to implementation details. Use public interfaces rather than accessing internal state, prefer mocked or fake data over external dependencies, and keep tests general rather than tightly coupled to specific implementations.

Key principles:
- Avoid accessing internal state like `raw_points` in test cases - use proper public interfaces like `handle_log` instead
- Use made-up or mocked data rather than requiring external handlers when the test doesn't specifically need to test that integration
- Design tests to know as little as possible about specific implementations (e.g., car brands) to keep them general and maintainable

Example of good practice:
```python
# Instead of accessing internal state:
est.raw_points["lat_active"].append(True)

# Use the public interface:
est.handle_log(log_message)
```

This approach makes tests more maintainable, less brittle to refactoring, and easier to understand by focusing on the component's public contract rather than its internal implementation.