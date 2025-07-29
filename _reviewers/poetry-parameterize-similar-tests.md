---
title: Parameterize similar tests
description: Use `pytest.mark.parametrize` to consolidate similar test cases instead
  of duplicating test code. This approach improves maintainability, reduces code duplication,
  and ensures comprehensive test coverage across different scenarios.
repository: python-poetry/poetry
label: Testing
language: Python
comments_count: 12
repository_stars: 33496
---

Use `pytest.mark.parametrize` to consolidate similar test cases instead of duplicating test code. This approach improves maintainability, reduces code duplication, and ensures comprehensive test coverage across different scenarios.

When you find yourself writing multiple test functions that follow the same pattern with different inputs or expected outputs, combine them into a single parameterized test. This makes it easier to add new test cases and ensures consistent testing logic.

Example of consolidating duplicate tests:

```python
# Instead of multiple similar tests:
def test_git_ref_spec_resolve_branch():
    refspec = GitRefSpec(branch="main")
    refspec.resolve(mock_fetch_pack_result)
    assert refspec.ref == b"refs/heads/main"

def test_git_ref_spec_resolve_tag():
    refspec = GitRefSpec(revision="v1.0.0")
    refspec.resolve(mock_fetch_pack_result)
    assert refspec.ref == annotated_tag(b"refs/tags/v1.0.0")

# Use parameterization:
@pytest.mark.parametrize("input_type,input_value,expected_ref", [
    ("branch", "main", b"refs/heads/main"),
    ("revision", "v1.0.0", annotated_tag(b"refs/tags/v1.0.0")),
    ("revision", "abc", b"refs/heads/main"),
])
def test_git_ref_spec_resolve(input_type, input_value, expected_ref):
    kwargs = {input_type: input_value}
    refspec = GitRefSpec(**kwargs)
    refspec.resolve(mock_fetch_pack_result)
    assert refspec.ref == expected_ref
```

This approach is particularly valuable when testing different error conditions, input formats, or configuration options. It also makes it easier to identify gaps in test coverage and add new test cases systematically.