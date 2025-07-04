---
title: Consistent configuration patterns
description: When working with configurations in Pydantic models, maintain consistency
  by using `ConfigDict()` instead of plain dictionaries for better type checking support
  and IDE assistance. This provides explicit typing and makes your configuration intentions
  clearer.
repository: pydantic/pydantic
label: Configurations
language: Markdown
comments_count: 4
repository_stars: 24377
---

When working with configurations in Pydantic models, maintain consistency by using `ConfigDict()` instead of plain dictionaries for better type checking support and IDE assistance. This provides explicit typing and makes your configuration intentions clearer.

```python
# Recommended - using ConfigDict for type checking support
from pydantic import BaseModel, ConfigDict

class Model(BaseModel):
    model_config = ConfigDict(str_max_length=10, validate_by_name=True)
    
    field: str
    
# Alternative approach - using class arguments (useful for 'frozen')
class FrozenModel(BaseModel, frozen=True):
    id: int
    name: str
```

Be aware of how configurations merge in inheritance hierarchies - child class settings override parent class settings for the same configuration keys. Document clearly which configurations are being overridden when implementing class inheritance.

Remember that runtime method parameters can override model configurations when explicitly provided, but default method parameters do not override model configurations. For example, when using validation methods, the default behavior follows the model configuration unless explicitly changed:

```python
# The model's configuration takes precedence unless explicitly overridden
model = Model.model_validate(data)  # Uses model_config settings
model = Model.model_validate(data, by_alias=False)  # Explicitly overrides config
```