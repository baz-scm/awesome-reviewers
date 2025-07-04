---
title: Organize tests efficiently
description: Write maintainable, well-structured tests that are easy to understand
  and extend. Tests should remain simple and focused on their specific validation
  purpose.
repository: pola-rs/polars
label: Testing
language: Python
comments_count: 4
repository_stars: 34296
---

Write maintainable, well-structured tests that are easy to understand and extend. Tests should remain simple and focused on their specific validation purpose.

Three key practices to follow:

1. **Use pytest parametrization** to express multiple test scenarios concisely rather than duplicating similar test functions:

```python
# Instead of multiple similar test functions:
def test_unique_counts_on_bool_only_true() -> None:
    s = pl.Series("bool", [True, True, True])
    expected = pl.Series("bool", [3], dtype=pl.UInt32)
    assert_series_equal(s.unique_counts(), expected)

def test_unique_counts_on_bool_only_false() -> None:
    s = pl.Series("bool", [False, False, False])
    expected = pl.Series("bool", [3], dtype=pl.UInt32)
    assert_series_equal(s.unique_counts(), expected)

# Prefer a single parametrized test:
@pytest.mark.parametrize(
    ("input", "expected"),
    [
        ([True, True, True], [3]),
        ([False, False, False], [3]),
        ([True, False, False, True, True], [3, 2]),
    ]
)
def test_unique_counts_bool(input: list[bool], expected: list[int]):
    assert_series_equal(
        pl.Series("bool", input).unique_counts(),
        pl.Series("bool", expected, dtype=pl.UInt32)
    )
```

2. **Avoid complex logic in test cases**. Each test should be straightforward and focused on specific validation. If a test contains intricate logic, consider refactoring into multiple simpler tests.

3. **Use appropriate test fixtures and environments**:
   - Use the `tmp_path` fixture for file operations instead of hardcoded paths
   - Prefer in-memory testing with `io.BytesIO()` over disk operations when possible for better performance
   - Ensure tests are isolated and don't interfere with each other