---
title: Document configuration relationships
description: When designing configuration options that interact with each other, clearly
  document these relationships and consider implementing safeguards against invalid
  combinations. This is especially important for boolean flags controlling related
  behaviors.
repository: pydantic/pydantic
label: Configurations
language: Python
comments_count: 4
repository_stars: 24377
---

When designing configuration options that interact with each other, clearly document these relationships and consider implementing safeguards against invalid combinations. This is especially important for boolean flags controlling related behaviors.

1. Document interdependencies explicitly in configuration documentation
2. Consider automatic adjustments when one setting implies another
3. Provide warnings when potentially conflicting values are detected

For example, in discussion #8, the `validate_by_alias` and `validate_by_name` settings have a critical relationship:

```python
class ConfigDict:
    validate_by_alias: bool
    """
    Whether an aliased field may be populated by its alias. Defaults to `True`.

    !!! tip
        If you set `validate_by_alias` to `False`, you should set `validate_by_name` to `True` 
        to ensure that the field can still be populated.
    """
    
    validate_by_name: bool
    """
    Whether a field may be populated by its name. Defaults to `False`.
    """
```

Consider adding automatic adjustments to handle common patterns:

```python
# When a user sets one configuration, automatically adjust related ones if needed
if config.get('validate_by_alias') is False and config.get('validate_by_name') is None:
    config['validate_by_name'] = True
    warnings.warn(
        'Setting validate_by_name=True automatically because validate_by_alias=False',
        UserWarning,
        stacklevel=2,
    )
```