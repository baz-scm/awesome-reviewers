---
title: Write targeted, specific tests
description: Tests should validate specific, well-defined behaviors with clear assertions
  that directly relate to what's being tested. Avoid writing overly general or unfocused
  tests that try to cover too much at once, as these are often harder to maintain
  and debug when they fail.
repository: pydantic/pydantic
label: Testing
language: Python
comments_count: 4
repository_stars: 24377
---

Tests should validate specific, well-defined behaviors with clear assertions that directly relate to what's being tested. Avoid writing overly general or unfocused tests that try to cover too much at once, as these are often harder to maintain and debug when they fail.

Good tests:
1. Have a clear, singular purpose evident from their name and implementation
2. Include specific assertions that validate exactly what you're testing
3. Provide helpful error messages that make failures easy to diagnose
4. Are separated by functionality rather than combining different test cases

For example, instead of writing a general test:

```python
# Too general and unfocused
def test_model_attributes():
    model = Model()
    # Testing too many things at once
    assert model.field == "default"
    assert model._private_attr is not None
    assert callable(model.method)
```

Write specific, targeted tests:

```python
def test_private_attribute_not_skipped_during_ns_inspection() -> None:
    # Clear comment explaining the test's purpose
    # It is important for the enum name to start with the class name
    # (it previously caused issues with qualname comparisons):
    class Fullname(str, Enum):
        pass

    class Full(BaseModel):
        _priv: object = Fullname

    # Specific assertion testing exactly one behavior
    assert isinstance(Full._priv, ModelPrivateAttr)
```

When parameterizing tests, ensure each parameter set tests a distinct case that belongs together. If test cases require different assertion logic or warning checks, they should be in separate test functions.