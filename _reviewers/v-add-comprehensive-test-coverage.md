---
title: Add comprehensive test coverage
description: When adding functionality or fixing bugs, always add new test functions
  rather than modifying existing ones to preserve test coverage. Ensure comprehensive
  testing by including edge cases, error conditions, and assertions for all public
  functions. Use meaningful, non-default values in tests to improve sensitivity to
  regressions.
repository: vlang/v
label: Testing
language: Other
comments_count: 13
repository_stars: 36582
---

When adding functionality or fixing bugs, always add new test functions rather than modifying existing ones to preserve test coverage. Ensure comprehensive testing by including edge cases, error conditions, and assertions for all public functions. Use meaningful, non-default values in tests to improve sensitivity to regressions.

Key practices:
- Add new test functions instead of modifying existing ones: "Please add new test functions, instead of modifying the existing ones, unless there is a bug. That makes reviewing a lot easier."
- Test edge cases and error conditions: "Please, also add another test_ function, that sets the mutable parameter to a value != none"
- Include proper assertions: "Please add assertions too" rather than just dumps or prints
- Test all public functions: "public functions should preferably have their own tests"
- Use non-default values: Use values like 1, 3, or 42 instead of 0, as "0 is not a good value for testing, because the default initialisation also uses 0s"
- Test both positive and negative cases: Include tests for both expected success and failure scenarios

Example:
```v
// Good: Adding new test function with comprehensive coverage
fn test_new_feature_success_case() {
    result := my_function(42) // Use meaningful non-zero value
    assert result == expected_value
}

fn test_new_feature_error_case() {
    if _ := my_function(-1) { 
        assert false 
    } else { 
        assert true 
    }
}

// Avoid: Modifying existing test functions or using only default values
```

This approach maintains existing test coverage while ensuring new functionality is thoroughly validated, making code reviews easier and preventing regressions.