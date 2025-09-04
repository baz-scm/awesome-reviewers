---
title: Test structure and clarity
description: Organize tests for maximum clarity and maintainability by leveraging
  pytest features and proper test structure. Split complex tests into focused, single-purpose
  test cases rather than testing multiple scenarios in one function. Use pytest fixtures
  for setup and cleanup instead of manual resource management, and prefer parameterization
  for testing multiple...
repository: stanfordnlp/dspy
label: Testing
language: Python
comments_count: 5
repository_stars: 27813
---

Organize tests for maximum clarity and maintainability by leveraging pytest features and proper test structure. Split complex tests into focused, single-purpose test cases rather than testing multiple scenarios in one function. Use pytest fixtures for setup and cleanup instead of manual resource management, and prefer parameterization for testing multiple inputs.

Key practices:
- Split multi-scenario tests: "shall we parameterize or split the test for clear test cases? Splitting sounds good to me"
- Use pytest fixtures for automatic cleanup: "use `tmp_path` fixture so that it's automatically cleaned up"
- Prefer helper functions over fixtures when appropriate: "we don't need this to be a fixture, we can just define the `dummy_embedder()` as a helper function"
- Separate integration tests from unit tests: "I think it is good to separate these integration and maybe later we want to run them in their own CI step"
- Use pytest-specific assertions: "Let's use pytest matcher rather than manually using `assert`"

Example of good test structure:
```python
@pytest.mark.parametrize("module", [dspy.Predict, dspy.ChainOfThought])
def test_color_classification_using_enum(module):
    # Single focused test case with parameterization
    
def test_file_access_control(tmp_path):
    # Use pytest fixture for automatic cleanup
    testfile_path = tmp_path / "test_file.txt"
```

This approach makes tests more readable, maintainable, and reliable while following pytest best practices.