---
title: Write clear test cases
description: 'Structure test cases for maximum readability and maintainability by
  following these principles:


  1. Organize each test in three distinct parts separated by blank lines:'
repository: Unstructured-IO/unstructured
label: Testing
language: Python
comments_count: 9
repository_stars: 12116
---

Structure test cases for maximum readability and maintainability by following these principles:

1. Organize each test in three distinct parts separated by blank lines:
   - Setup (arrange test fixtures)
   - Execution (run unit under test)
   - Verification (assert expected results)

2. Minimize intermediate variables - use direct assertions when possible:

Instead of:
```python
matrix = [["cell1", "cell2"], ["cell3", "cell4"]]
expected_html = "<table><tr><td>cell1</td>...</table>"
assert utils.htmlify_matrix(matrix) == expected_html
```

Prefer:
```python
assert utils.htmlify_matrix([["cell1", "cell2"], ["cell3", "cell4"]]) == (
    "<table><tr><td>cell1</td><td>cell2</td></tr>"
    "<tr><td>cell3</td><td>cell4</td></tr></table>"
)
```

3. Use parameterization to avoid repeated test code:
```python
@pytest.mark.parametrize(
    "date", ["1990-12-01", "2050-01-01T00:00:00", "2050-01-01+00:00:00"]
)
def test_validate_date_args_accepts_standard_formats(date):
    assert utils.validate_date_args(date)
```

4. Write meaningful assertions that clearly indicate the behavior being tested:
```python
# Weak assertion:
assert "error" in caplog.text

# Better assertion:
assert "invalid date format, expected YYYY-MM-DD" in caplog.text
```