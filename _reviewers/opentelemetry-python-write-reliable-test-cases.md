---
title: Write reliable test cases
description: 'Create deterministic and reliable test cases by following these guidelines:


  1. Use hardcoded values instead of random data to ensure reproducibility:'
repository: open-telemetry/opentelemetry-python
label: Testing
language: Python
comments_count: 4
repository_stars: 2061
---

Create deterministic and reliable test cases by following these guidelines:

1. Use hardcoded values instead of random data to ensure reproducibility:
```python
# Bad
boundaries = [randint(0, 1000)]

# Good
boundaries = [500]  # Fixed, predictable value
```

2. For timing-sensitive tests:
- Mark tests as flaky if they depend on timing:
```python
@mark.flaky(reruns=3, reruns_delay=1)
def test_timing_dependent():
    # Test implementation
```
- Use precise assertions for time comparisons:
```python
# Bad
self.assertTrue((after_export - before_export) < 1e9)

# Good
self.assertLess(after_export - before_export, 1e9)
# or
self.assertAlmostEqual(after_export - before_export, expected, delta=1e9)
```

3. Skip platform-specific tests rather than adding workarounds:
```python
@mark.skipif(
    system() == "Windows",
    reason="Tests fail due to Windows time_ns resolution limitations"
)
def test_platform_specific():
    # Test implementation
```

These practices ensure tests are reproducible, maintainable, and provide clear failure messages when issues occur.