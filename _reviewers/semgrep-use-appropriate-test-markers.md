---
title: use appropriate test markers
description: Test markers and annotations should match the test type and context they're
  applied to. Different test categories (unit tests, e2e tests, integration tests)
  require different markers to ensure proper test organization and execution.
repository: semgrep/semgrep
label: Testing
language: Python
comments_count: 2
repository_stars: 12598
---

Test markers and annotations should match the test type and context they're applied to. Different test categories (unit tests, e2e tests, integration tests) require different markers to ensure proper test organization and execution.

For example, markers like `osemfail` and `no_semgrep_cli` are typically meant for end-to-end tests and should not be applied to unit tests. When adding new functionality, use markers that indicate the test's purpose and any special requirements for porting or execution.

```python
# Incorrect - using e2e markers on unit tests
@pytest.mark.quick
@pytest.mark.no_semgrep_cli  # Remove - not relevant for unit tests
@pytest.mark.osemfail       # Remove - not relevant for unit tests
def test_clean_project_url():
    pass

# Correct - using appropriate markers for the test context
@pytest.mark.quick
def test_clean_project_url():
    pass

# Correct - using osemfail for tests that need porting
@pytest.mark.osemfail  # Appropriate when test needs to be ported
def test_metrics_filtering():
    pass
```

This ensures tests are properly categorized, executed in the right contexts, and that CI/CD pipelines can correctly identify and run the appropriate test suites.