---
title: Semantic over syntactic
description: Choose names that clearly communicate the purpose and behavior of your
  code elements, focusing on semantic meaning rather than just syntax. Names should
  instantly convey what something is or does without requiring readers to investigate
  implementation details.
repository: pydantic/pydantic
label: Naming Conventions
language: Python
comments_count: 4
repository_stars: 24377
---

Choose names that clearly communicate the purpose and behavior of your code elements, focusing on semantic meaning rather than just syntax. Names should instantly convey what something is or does without requiring readers to investigate implementation details.

For properties and variables:
- Use nouns that represent what the data is, not how it's implemented
- Avoid names that suggest actions when they're actually retrieving data

```python
# Misleading - suggests an action of setting constraints
@property
def set_constraints(self) -> dict[str, Any]: ...

# Better - clearly indicates a property that returns defined constraints
@property
def defined_constraints(self) -> dict[str, Any]: ...
```

For functions and classes:
- Make names specific enough to differentiate from similar entities
- Add clarifying words to prevent ambiguity

```python
# Unclear - what kind of "invalid" is this?
class CollectedInvalid(Exception): ...

# Better - clearly indicates the domain and purpose
class CollectedInvalidSchema(Exception): ...
```

For type variables and parameters:
- Use descriptive names that indicate their purpose

```python
# Cryptic - what is R used for?
_R = TypeVar('_R')

# Better - indicates the purpose of the type variable
ReturnType = TypeVar('ReturnType')
```

Names that accurately reflect semantics make code more maintainable, self-documenting, and less prone to misuse.