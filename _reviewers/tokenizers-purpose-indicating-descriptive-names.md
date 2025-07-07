---
title: Purpose-indicating descriptive names
description: Choose names for variables, methods, parameters, and fixtures that clearly
  communicate their purpose, content, and behavior. Names should be self-documenting
  and consider future code evolution.
repository: huggingface/tokenizers
label: Naming Conventions
language: Python
comments_count: 3
repository_stars: 9868
---

Choose names for variables, methods, parameters, and fixtures that clearly communicate their purpose, content, and behavior. Names should be self-documenting and consider future code evolution.

For method names:
- Use action verbs that precisely describe the method's effect
- Prefer established patterns like `enable_xxx()`/`disable_xxx()` over ambiguous patterns like `with_xxx()`/`without_xxx()`

```python
# Less clear:
def with_padding(self, direction="right", ...):
    # ...

# More clear:
def enable_padding(self, direction="right", ...):
    # ...
```

For variables and parameters:
- Choose names that describe what the value represents rather than its implementation details
- Consider how names will work with future extensions

```python
# Less descriptive - unclear what these files contain:
@pytest.fixture(scope="session")
def precompiled_files(data_dir):
    # ...

# More descriptive - clearly indicates purpose and content:
@pytest.fixture(scope="session")
def serialized_files(data_dir):
    # ...
```

Maintain consistency in parameter naming across similar implementations to establish predictable patterns for API users.