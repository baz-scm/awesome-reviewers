---
title: Use modern assertions
description: Always use current assertion methods in test code to ensure clarity and
  future compatibility. Specifically, replace deprecated methods with their modern
  equivalents, such as using `assertRaisesRegex` instead of `assertRaisesRegexp` when
  validating exceptions. This approach allows you to verify both the exception type
  and the specific error message content...
repository: tensorflow/tensorflow
label: Testing
language: Python
comments_count: 2
repository_stars: 190625
---

Always use current assertion methods in test code to ensure clarity and future compatibility. Specifically, replace deprecated methods with their modern equivalents, such as using `assertRaisesRegex` instead of `assertRaisesRegexp` when validating exceptions. This approach allows you to verify both the exception type and the specific error message content in a single assertion.

```python
# Bad
with self.assertRaisesRegexp(ValueError, "expected message"):
    function_that_raises()

# Good
with self.assertRaisesRegex(ValueError, "expected message"):
    function_that_raises()
```

By using modern assertion methods, you improve test readability and maintainability while ensuring your tests will continue to work with future framework updates.