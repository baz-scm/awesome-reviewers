---
title: avoid external test dependencies
description: Tests should not rely on external URLs, live websites, or internet connectivity
  to ensure reliability, consistency, and faster execution. External dependencies
  can cause tests to fail due to network issues, website changes, or unavailability,
  making CI/CD pipelines unstable.
repository: browser-use/browser-use
label: Testing
language: Python
comments_count: 4
repository_stars: 69139
---

Tests should not rely on external URLs, live websites, or internet connectivity to ensure reliability, consistency, and faster execution. External dependencies can cause tests to fail due to network issues, website changes, or unavailability, making CI/CD pipelines unstable.

Instead of using live URLs, use these alternatives:
- **pytest-httpserver**: Create local HTTP servers for testing HTTP interactions
- **Local browser pages**: Use `chrome://version`, `about:blank`, or similar built-in pages
- **Self-contained test pages**: Create local HTML files or inline content for testing

Example of problematic code:
```python
await page.goto('https://example.com')  # External dependency
await page.goto('https://browserleaks.com/javascript')  # External dependency
```

Example of improved code:
```python
# Use pytest-httpserver (see test_controller.py)
await page.goto(f'http://localhost:{server.port}/test-page')

# Or use local browser pages
await page.goto('about:blank')
await page.goto('chrome://version')
```

This approach eliminates external dependencies, makes tests more reliable, reduces execution time, and ensures consistent results across different environments and network conditions.