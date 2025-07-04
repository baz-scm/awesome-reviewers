---
title: Preserve language conventions
description: 'When designing APIs that bridge between programming languages and external
  data formats (like JSON, XML, etc.), maintain language-specific naming conventions
  in your code while using aliases to accommodate external data formats. For Python
  APIs:'
repository: pydantic/pydantic
label: API
language: Markdown
comments_count: 3
repository_stars: 24377
---

When designing APIs that bridge between programming languages and external data formats (like JSON, XML, etc.), maintain language-specific naming conventions in your code while using aliases to accommodate external data formats. For Python APIs:

1. Use `snake_case` for internal field names following Python conventions
2. Define aliases for external formats that use different conventions (e.g., `camelCase` in JSON)
3. Document methods clearly with parentheses in references (e.g., `model_dump()` not just `model_dump`)
4. Present JSON examples with proper formatting for readability

Example:
```python
from pydantic import BaseModel, Field

class UserProfile(BaseModel):
    user_id: int = Field(validation_alias="userId", serialization_alias="userId") 
    first_name: str = Field(validation_alias="firstName", serialization_alias="firstName")
    
    # Python-native usage in code
    # user = UserProfile(user_id=1, first_name="John")
    
    # External data validation (JSON)
    # user = UserProfile.model_validate({"userId": 1, "firstName": "John"})
    
    # Example of well-formatted JSON output in documentation
    # import json
    # print(json.dumps(user.model_dump(by_alias=True), indent=2))
    # """
    # {
    #   "userId": 1,
    #   "firstName": "John"
    # }
    # """
```

This approach creates a clear separation between your language-specific implementation and external API contracts, improving code readability while maintaining compatibility with external systems. It also ensures your API documentation is consistent and easily understood by developers.