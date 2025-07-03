---
title: Use pytest parameterization
description: Structure unit tests using pytest's parameterize decorator instead of
  manual loops or wrapper functions. This approach improves test readability, makes
  failure cases easier to identify, and allows individual test cases to be run separately.
repository: apache/mxnet
label: Testing
language: Python
comments_count: 2
repository_stars: 20801
---

Structure unit tests using pytest's parameterize decorator instead of manual loops or wrapper functions. This approach improves test readability, makes failure cases easier to identify, and allows individual test cases to be run separately.

When implementing tests with multiple inputs or configurations:

1. Replace manual iteration through test cases with `@pytest.mark.parametrize()` decorators
2. Use multiple parametrize decorators when testing combinations of parameters
3. Use pytest's built-in exception testing utilities for cleaner code

Example refactoring:

```python
# Before - manual iteration
def test_operation():
    test_cases = [
        (5, 10, True),
        (3, 7, False),
        (0, 1, True)
    ]
    
    for a, b, expected in test_cases:
        result = operation(a, b)
        assert result == expected

# After - pytest parameterization
@pytest.mark.parametrize('a,b,expected', [
    (5, 10, True),
    (3, 7, False),
    (0, 1, True)
])
def test_operation(a, b, expected):
    result = operation(a, b)
    assert result == expected
```

This approach makes tests more maintainable, documents test cases more clearly, and provides better reporting when tests fail by clearly identifying which specific parameter combination caused the failure.
