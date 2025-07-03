---
title: Test comprehensively and systematically
description: Write comprehensive tests that validate both new functionality and edge
  cases, and organize them systematically to improve maintainability. When adding
  features or making changes, include tests that would catch regressions, and prefer
  extending existing test suites over creating isolated test cases.
repository: pytorch/pytorch
label: Testing
language: Python
comments_count: 7
repository_stars: 91169
---

Write comprehensive tests that validate both new functionality and edge cases, and organize them systematically to improve maintainability. When adding features or making changes, include tests that would catch regressions, and prefer extending existing test suites over creating isolated test cases.

Key practices:
1. **Test all code changes**: Every PR should include appropriate test coverage
   ```python
   # When adding functionality like this:
   def validate(x: T) -> Union[T, FakeTensor]:
       nonlocal flat_arg_fake_tensors
       if not self.is_our_fake(x):
           # ...
   
   # Include tests to verify the functionality:
   def test_validate_function():
       # Test the happy path
       # Test edge cases
       # Test error conditions
   ```

2. **Organize tests logically**: Add tests to the most appropriate existing file rather than creating one-off test files
   ```python
   # Instead of creating a new file:
   # test_deserialize_torch_artifact_dict.py
   
   # Add to the relevant existing file:
   # test_serialize.py -> test_deserialize_torch_artifact_dict()
   ```

3. **Extend generic tests**: Update generic test methods to cover new cases rather than creating separate specific tests
   ```python
   # Instead of:
   def test_take_along_dim_negative_indices(self) -> None:
       # Test specific case
   
   # Add test cases to the generic test:
   # Update test values in common_methods_invocations.py
   ```

4. **Reuse test infrastructure**: Extract common setup into helper methods or setUp methods
   ```python
   # Instead of repetitive setup in every test:
   def test_dynamic_shapes_run(self):
       torch._dynamo.reset()
       torch._dynamo.config.dynamic_shapes = True
       # Test logic...
   
   # Move common setup to setUp:
   def setUp(self):
       torch._dynamo.reset()
       torch._dynamo.config.dynamic_shapes = True
   ```

By following these practices, you'll create tests that serve as both validation and documentation, ensuring your code remains robust across changes and is easier for others to understand and maintain.
