---
title: Follow flake8 style guidelines
description: 'Adhere to the project''s established flake8 style guidelines as defined
  in setup.cfg. This includes:


  1. Maintain line length limits of 80 characters for consistency and readability
  across all files.'
repository: boto/boto3
label: Code Style
language: Other
comments_count: 2
repository_stars: 9417
---

Adhere to the project's established flake8 style guidelines as defined in setup.cfg. This includes:

1. Maintain line length limits of 80 characters for consistency and readability across all files.
2. Use proper vertical spacing in Python code, with two blank lines between top-level elements (classes and functions) to satisfy E302 requirements.

```python
# Incorrect - exceeds 80 character line limit
def some_function(parameter1, parameter2, parameter3, parameter4, parameter5, parameter6, very_long_parameter):
    return True

# Incorrect - missing blank lines between top-level elements
import boto3
def example_function():
    pass
class ExampleClass:
    pass

# Correct formatting
import boto3

def example_function():
    pass

class ExampleClass:
    pass
```

Remember that these style checks are enforced both in local development and by the CI "Lint" workflow. Following these conventions consistently improves code readability and prevents CI failures.