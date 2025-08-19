---
title: Test edge cases comprehensively
description: Ensure your tests cover not just the happy path, but also edge cases,
  empty states, error conditions, and boundary scenarios. This includes testing with
  empty datasets, validating pagination logic, handling unusual input values, and
  verifying error handling behavior.
repository: PostHog/posthog
label: Testing
language: Python
comments_count: 2
repository_stars: 28460
---

Ensure your tests cover not just the happy path, but also edge cases, empty states, error conditions, and boundary scenarios. This includes testing with empty datasets, validating pagination logic, handling unusual input values, and verifying error handling behavior.

When writing tests, systematically consider:
- Empty or null inputs (empty models, missing data)
- Boundary conditions (timezone edge cases like +5:30 offsets)
- Error scenarios and exception handling
- Pagination and query logic validation

Example from the discussions:
```python
def test_recent_activity_includes_external_jobs_and_modeling_jobs(self):
    # Don't just test the happy path - also test:
    # - Empty states (if either model is empty)
    # - Pagination works correctly
    # - Query logic handles edge cases properly
```

```python
def test_timezone_edge_cases(self):
    # Test unusual timezone offsets like India +5:30
    # Even if it's to assert that something throws an error
```

Comprehensive edge case testing catches bugs early, validates assumptions about system behavior, and ensures robust handling of real-world scenarios that may not be immediately obvious during development.